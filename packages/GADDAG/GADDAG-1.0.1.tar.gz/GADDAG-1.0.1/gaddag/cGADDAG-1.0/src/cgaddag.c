/*
 * This is an implementation of a semi-minimized GADDAG, as described in `A
 * Faster Scrabble Move Generation Algorithm' (Gordon, 1994).
 *
 * To support a large lexicon with fast lookups, the GADDAG is implemented as
 * 2D array of 32-bit unsigned integers, indexed by node number then edge
 * character, leading to a new node in the graph. Non-existent edges lead to
 * node 0, the root node of the trie. Letter sets are implemented as an array
 * of 32-bit unsigned integers, treated as a bitfield, indexed by node number.
 * The size of the bitfield limits the number of characters which the GADDAG
 * can support. It currently allows for 27 characters: the 26 characters of the
 * lowercase English alphabet, and the break character (`+'). There are 5 bits
 * left unused in the bitfield. By limiting the character set to lowercase, the
 * GADDAG becomes case-insensitive.
 */
#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef COMPRESSION
#include <zlib.h>
#endif

#include "cgaddag.h"


const uint32_t GDG_CAP = 100;
const uint32_t GDG_MAX_CHARS = 27;

/*
 * Internal function prototypes.
 */

static int gdg_ch_to_idx(char ch);
static char gdg_idx_to_ch(uint8_t idx);
static bool gdg_grow(GADDAG *gdg, uint32_t new_cap);
static uint32_t gdg_add_edge(GADDAG *gdg, uint32_t node, char ch);
static bool gdg_force_edge(GADDAG *gdg, uint32_t node, char ch, uint32_t dst);
static void gdg_set_edge(GADDAG *gdg, uint32_t node, char ch, uint32_t dst);
static uint32_t gdg_add_final_edge(GADDAG *gdg, uint32_t node, char ch,
                                   char end_ch);
static void gdg_add_end(GADDAG *gdg, uint32_t node, char ch);
static Result * gdg_create_result(const char *str, Result* next);
static Result * gdg_crawl(const GADDAG *gdg, const uint32_t node,
                          const char *partial_word, Result *res,
                          const bool wrap, const bool append);

/*
 * External interface.
 */

GADDAG *
gdg_create(void)
{
	GADDAG *gdg = NULL;

	gdg = malloc(sizeof(struct GADDAG_Struct));
	if (gdg == NULL)
		return NULL;

	gdg->cap = GDG_CAP;
	gdg->edges = calloc(GDG_MAX_CHARS * gdg->cap, sizeof(uint32_t));
	gdg->letter_sets = calloc(gdg->cap, sizeof(uint32_t));
	gdg->num_words = 0;
	gdg->num_nodes = 1;
	gdg->num_edges = 0;

	return gdg;
}

off_t
gdg_save(const GADDAG *gdg, const char *path)
{
	off_t total_wrote = 0;
	size_t size = sizeof(uint32_t);
	FILE *fp = NULL;

	fp = fopen(path, "wb");
	if (fp == NULL)
		return -1;

	total_wrote += fwrite(&gdg->cap, size, 1, fp);
	total_wrote += fwrite(&gdg->num_words, size, 1, fp);
	total_wrote += fwrite(&gdg->num_nodes, size, 1, fp);
	total_wrote += fwrite(&gdg->num_edges, size, 1, fp);
	total_wrote += fwrite(gdg->edges, size, gdg->cap * GDG_MAX_CHARS, fp);
	total_wrote += fwrite(gdg->letter_sets, size, gdg->cap, fp);
	total_wrote *= size;

	fclose(fp);

	return total_wrote;
}

#ifdef COMPRESSION
off_t
gdg_save_compressed(const GADDAG *gdg, const char *path)
{
	off_t total_wrote = 0;
	size_t size = sizeof(uint32_t);
	gzFile fp = NULL;

	fp = gzopen(path, "wb");
	if (fp == NULL)
		return -1;

	total_wrote += gzwrite(fp, &gdg->cap, size);
	total_wrote += gzwrite(fp, &gdg->num_words, size);
	total_wrote += gzwrite(fp, &gdg->num_nodes, size);
	total_wrote += gzwrite(fp, &gdg->num_edges, size);
	total_wrote += gzwrite(fp, gdg->edges, size * gdg->cap * GDG_MAX_CHARS);
	total_wrote += gzwrite(fp, gdg->letter_sets, size * gdg->cap);

	gzclose(fp);

	return total_wrote;
}
#endif

/* The gz* functions handle both compressed and uncompressed files. */
#ifdef COMPRESSION
#define FILE_T gzFile
#define OPEN gzopen
#define READ(fp, dst, sz) gzread((fp), (dst), (sz))
#define CLOSE gzclose
#else
#define FILE_T FILE*
#define OPEN fopen
#define READ(fp, dst, sz) fread((dst), (sz), 1, (fp))
#define CLOSE fclose
#endif
GADDAG *
gdg_load(const char *path)
{
	GADDAG *gdg = NULL;
	size_t size = sizeof(uint32_t);
	FILE_T fp = NULL;
	uint32_t cap = 0;

	gdg = gdg_create();
	if (gdg == NULL)
		return NULL;

	fp = OPEN(path, "rb");
	if (fp == NULL) {
		gdg_destroy(gdg);
		return NULL;
	}

	READ(fp, &cap, size);
	gdg_grow(gdg, cap);

	READ(fp, &gdg->num_words, size);
	READ(fp, &gdg->num_nodes, size);
	READ(fp, &gdg->num_edges, size);
	READ(fp, gdg->edges, size * gdg->cap * GDG_MAX_CHARS);
	READ(fp, gdg->letter_sets, size * gdg->cap);

	CLOSE(fp);

	return gdg;
}
#undef FILE_T
#undef OPEN
#undef READ
#undef CLOSE

void
gdg_destroy(GADDAG *gdg)
{
	free(gdg->edges);
	free(gdg->letter_sets);
	free(gdg);
}

int
gdg_add_word(GADDAG *gdg, const char *word)
{
	const size_t len = strlen(word);
	uint32_t node = 0;

	/* Check for any characters not in the character set. */
	for (size_t i = 0; i < len; i++) {
		if (gdg_ch_to_idx(word[i]) == -1)
			return 1;
	}

	gdg->num_words++;

	/* Add path from last letter in word. */
	for (int i = len - 1; i >= 2; --i) {
		node = gdg_add_edge(gdg, node, word[i]);
		if (node == 0)
			return 2;
	}
	node = gdg_add_final_edge(gdg, node, word[1], word[0]);
	if (node == 0)
		return 2;

	/* Return early if word is a single character. */
	if (len == 1)
		return 0;

	/* Add path from penultimate letter in word. */
	node = 0;
	for (int i = len - 2; i >= 0; --i) {
		node = gdg_add_edge(gdg, node, word[i]);
		if (node == 0)
			return 2;
	}
	node = gdg_add_final_edge(gdg, node, '+', word[len - 1]);
	if (node == 0)
		return 2;

	/* Create remaining semi-minimized paths. */
	for (int m = len - 3; m >= 0; --m) {
		const uint32_t force_node = node;
		node = 0;

		for (int i = m; i >= 0; --i) {
			node = gdg_add_edge(gdg, node, word[i]);
			if (node == 0)
				return 2;
		}

		node = gdg_add_edge(gdg, node, '+');
		if (node == 0 ||
		    !gdg_force_edge(gdg, node, word[m + 1], force_node))
			return 2;
	}

	return 0;
}

bool
gdg_has(const GADDAG *gdg, const char *word)
{
	uint32_t node = 0;

	for (int i = strlen(word) - 1; i > 0; --i) {
		node = gdg_follow_edge(gdg, node, word[i]);
		if (node == 0)
			return false;
	}

	return gdg_is_end(gdg, node, word[0]);
}

Result *
gdg_starts_with(const GADDAG *gdg, const char *prefix)
{
	Result *res = NULL;
	uint32_t node = 0;

	for (int i = strlen(prefix) - 1; i >= 0; --i) {
		if (i == 0 && gdg_is_end(gdg, node, prefix[i]))
			res = gdg_create_result(prefix, NULL);

		node = gdg_follow_edge(gdg, node, prefix[i]);
		if (node == 0)
			return NULL;
	}

	node = gdg_follow_edge(gdg, node, '+');
	if (node == 0)
		return NULL;

	return gdg_crawl(gdg, node, prefix, res, false, true);
}

Result *
gdg_contains(const GADDAG *gdg, const char *sub)
{
	Result *res = NULL;
	uint32_t node = 0;

	for (int i = (strlen(sub) - 1); i >= 0; --i) {
		if (i == 0 && gdg_is_end(gdg, node, sub[i]))
			res = gdg_create_result(sub, NULL);

		node = gdg_follow_edge(gdg, node, sub[i]);
		if (node == 0)
			return NULL;
	}

	return gdg_crawl(gdg, node, sub, res, true, false);
}

Result *
gdg_ends_with(const GADDAG *gdg, const char *suffix)
{
	Result *res = NULL;
	uint32_t node = 0;

	for (int i = strlen(suffix) - 1; i >= 0; --i) {
		if (i == 0 && gdg_is_end(gdg, node, suffix[i]))
			res = gdg_create_result(suffix, NULL);

		node = gdg_follow_edge(gdg, node, suffix[i]);
		if (node == 0)
			return NULL;
	}

	return gdg_crawl(gdg, node, suffix, res, false, false);
}

int
gdg_edges(const GADDAG *gdg, const uint32_t node, char *buf)
{
	uint8_t n = 0;
	uint8_t i = 0;

	for (int j = 0; j < GDG_MAX_CHARS; j++) {
		const char ch = gdg_idx_to_ch(j);
		const uint32_t next_node = gdg_follow_edge(gdg, node, ch);

		if (next_node != 0) {
			n++;
			if (buf != NULL)
				buf[i++] = ch;
		}
	}

	return n;
}

int
gdg_letter_set(const GADDAG *gdg, const uint32_t node, char *buf)
{
	uint8_t n = 0;
	uint8_t i = 0;

	for (int j = 1; j < GDG_MAX_CHARS; j++) {
		if ((gdg->letter_sets[node] >> j) & 1) {
			n++;
			if (buf != NULL)
				buf[i++] = gdg_idx_to_ch(j);
		}
	}

	return n;
}

bool
gdg_is_end(const GADDAG *gdg, const uint32_t node, const char ch)
{
	const int ch_idx = gdg_ch_to_idx(ch);

	if (ch_idx == -1)
		return false;
	else
		return gdg->letter_sets[node] & (1 << ch_idx);
}

uint32_t
gdg_follow_edge(const GADDAG *gdg, const uint32_t node, const char ch)
{
	const int ch_idx = gdg_ch_to_idx(ch);

	if (ch_idx == -1)
		return 0;
	else
		return gdg->edges[node * GDG_MAX_CHARS + ch_idx];
}

void
gdg_destroy_result(Result *res)
{
	Result *tmp = res;
	Result *last = NULL;

	/* Find end of linked list. */
	while (tmp != NULL) {
		last = tmp;
		tmp = tmp->next;
	}

	/* Free nodes of linked list, starting from the end. */
	while (last != NULL) {
		Result *prev = last->prev;

		free((char*)(last->str));
		free((Result*)last);

		last = prev;
	}
}

/* Internal functions. */

/**
 * \brief Converts a character into an index.
 *
 * After converting the character to lowercase, returns its index.
 *
 * \param ch Character to convert to an index.
 *
 * \return Index for a character.
 *
 * \retval -1 Invalid character.
 */
static int
gdg_ch_to_idx(const char ch)
{
	const char ch_low = tolower(ch);

	if (ch_low == '+')
		return 0;
	else if (ch_low >= 97 && ch_low <= 122)
		return ch_low - 96;
	else
		return -1;
}

/**
 * \brief Converts an index into a character.
 *
 * Returns the lowercase character represented by an index.
 *
 * \param idx Character to convert to an index.
 *
 * \return Character represented by an index.
 *
 * \retval 0 Invalid index.
 */
static char
gdg_idx_to_ch(const uint8_t idx)
{
	if (idx == 0)
		return '+';
	else if (idx >= 1 && idx <= 27)
		return idx + 96;
	else
		return '\0';
}

/**
 * \brief Increases the capacity of a GADDAG.
 *
 * Grows a GADDAG to a new capacity, which must be higher than its current
 * capacity, by reallocating its internal matrices.
 *
 * \param new_cap New capacity.
 *
 * \return Boolean indicating whether the GADDAG was successfully grown or not.
 *
 * \retval true GADDAG's capacity was successfully increased.
 * \retval false GADDAG's capacity was not successfully increased. If this was
 *               not due to the new capacity being smaller than the current
 *               capacity, the GADDAG is now in an undefined state.
 */
static bool
gdg_grow(GADDAG *gdg, const uint32_t new_cap)
{
	uint32_t old_cap = gdg->cap;
	size_t new_node_size = 0;
	size_t new_node_diff = 0;
	size_t new_edge_size = 0;
	size_t new_edge_diff = 0;
	uint32_t *new_edges = NULL;
	uint32_t *new_letter_sets = NULL;

	if (new_cap == old_cap)
		return true;
	else if (new_cap < old_cap)
		return false;

	gdg->cap = new_cap;

	new_node_size = new_cap * sizeof(uint32_t);
	new_node_diff = (new_cap - old_cap) * sizeof(uint32_t);
	new_edge_size = new_node_size * GDG_MAX_CHARS;
	new_edge_diff = new_node_diff * GDG_MAX_CHARS;

	new_edges = realloc(gdg->edges, new_edge_size);
	if (new_edges == NULL)
		return false;
	else
		gdg->edges = new_edges;
	memset(gdg->edges + old_cap * GDG_MAX_CHARS, 0, new_edge_diff);

	new_letter_sets = realloc(gdg->letter_sets, new_node_size);
	if (new_letter_sets == NULL)
		return false;
	else
		gdg->letter_sets = new_letter_sets;
	memset(gdg->letter_sets + old_cap, 0, new_node_diff);

	return true;
}

/**
 * \brief Adds an edge to a node, if it does not already exist.
 *
 * Adds an edge to a node leading to a _new_ node, returning the new node.
 * If the edge already exists, the node reached by follow that edge is returned
 * and no new edges or nodes are created.
 *
 * \param gdg GADDAG which contains the node.
 * \param node Node to add edge to.
 * \param ch Edge to add to node.
 *
 * \return Node reached by following the edge, can be a new or existing node.
 *
 * \retval 0 Failed to grow GADDAG to hold new node. The GADDAG is in an
 *           undefined state.
 */
static uint32_t
gdg_add_edge(GADDAG *gdg, const uint32_t node, const char ch)
{
	uint32_t dst = 0;

	if ((dst = gdg_follow_edge(gdg, node, ch)) == 0) {
		dst = gdg->num_nodes++;
		if (gdg->num_nodes >= gdg->cap) {
			if (!gdg_grow(gdg, gdg->cap + GDG_CAP))
				return 0;
		}
		gdg_set_edge(gdg, node, ch, dst);
	}

	return dst;
}

/**
 * \brief Adds a _new_ edge to a node leading to an _existing_ node.
 *
 * Adds a _new_ edge to a node leading to an _existing_ node. The edge cannot
 * already exist and lead to any node other than the specified node. Success or
 * failure to set the edge to the specified node is returned.
 *
 * \param gdg GADDAG which contains the node.
 * \param node Node to add edge to.
 * \param ch Edge to add to node.
 * \param dst Node edge should lead to.
 *
 * \return Boolean indicating whether the edge could be set to the specified
 *         node or not.
 *
 * \retval true An edge was created, or already exist, to the specified node.
 * \retval false Edge already exists and does not lead to the specified node.
 */
static bool
gdg_force_edge(GADDAG *gdg, const uint32_t node, const char ch,
               const uint32_t dst)
{
	uint32_t next_node = 0;

	if ((next_node = gdg_follow_edge(gdg, node, ch)) != dst)
	{
		if (next_node != 0)
			return false;
		gdg_set_edge(gdg, node, ch, dst);
	}

	return true;
}

/**
 * \brief Sets an edge from one node to another.
 *
 * Sets an edge on a node to an existing node, overwriting any existing edge,
 * if one already exists. The edge character is converted to lowercase.
 *
 * \param gdg GADDAG which contains the node.
 * \param node Node to add edge to.
 * \param ch Edge to add to node.
 * \param dst Node edge should lead to.
 */
static void
gdg_set_edge(GADDAG *gdg, const uint32_t node, const char ch,
             const uint32_t dst)
{
	const int ch_idx = gdg_ch_to_idx(ch);

	gdg->edges[node * GDG_MAX_CHARS + ch_idx] = dst;
	gdg->num_edges++;
}

/**
 * \brief Adds an edge to a node and a character to the end node's letter set.
 *
 * Adds an edge to a node leading to a _new_ node with a character in its
 * letter set, returning the new node. If the edge already exists, the
 * character is added to the letter set of the node reached by following that
 * edge and that node is returned.
 *
 * \param gdg GADDAG which contains the node.
 * \param node Node to add edge to.
 * \param ch Edge to add to node.
 * \param end_ch Character to add to new or existing node's letter set.
 *
 * \return Node reached by following the edge, can be a new or existing node.
 *
 * \retval 0 Failed to grow GADDAG to hold new node. The GADDAG is in an
 *           undefined state.
 */
static uint32_t
gdg_add_final_edge(GADDAG *gdg, const uint32_t node, const char ch,
                   const char end_ch)
{
	uint32_t dst = gdg_add_edge(gdg, node, ch);

	gdg_add_end(gdg, dst, end_ch);

	return dst;
}

/**
 * \brief Adds a character to a node's letter set.
 *
 * Adds a character to a node's letter set. The character is converted to
 * lowercase.
 *
 * \param gdg GADDAG which contains the node.
 * \param node Node to have its letter set added to.
 * \param ch Character to add to node's letter set.
 */
static void
gdg_add_end(GADDAG *gdg, const uint32_t node, const char ch)
{
	const int ch_idx = gdg_ch_to_idx(ch);

	gdg->letter_sets[node] |= (1 << ch_idx);
}

/**
 * \brief Creates a new Result.
 *
 * Allocates a new Result structure on the heap, storing _a copy_ of a string.
 * Can be added to the _front_ of an existing Result list.
 *
 * \param str String to store in the result.
 * \param next Existing Result list to prepend the new Result to.
 *
 * \return The new Result, at the head of the Result list.
 *
 * \retval NULL Failed to allocate memory for the Result.
 */
static Result *
gdg_create_result(const char *str, Result* next)
{
	Result* res = NULL;

	if ((res = malloc(sizeof(struct Result_Struct))) == NULL)
		return NULL;

	if (next != NULL)
		next->prev = res;

	res->str = strdup(str);
	res->next = next;
	res->prev = NULL;

	if (res->str == NULL)
		return NULL;

	return res;
}

/**
 * \brief Finds all possible words starting from a node.
 *
 * Crawl all edges of a node and subsequent nodes to find all words.
 *
 * \param gdg GADDAG to crawl.
 * \param node Node to start crawling from.
 * \param partial_word Current partial word built from crawling.
 * \param res Existing Result list to prepend the new Result to.
 * \param wrap "Wrap" by following the break edge.
 * \param append Characters now form the suffix and should added to the end.
 *
 * \return The head of a Result list containing all found words.
 *
 * \retval NULL Failed to allocate memory.
 */
static Result *
gdg_crawl(const GADDAG *gdg, const uint32_t node, const char *partial_word,
          Result *res, const bool wrap, const bool append)
{
	const size_t len = strlen(partial_word);
	const uint8_t start_idx = wrap ? 0 : 1;

	for (uint32_t i = start_idx; i < GDG_MAX_CHARS; i++)
	{
		const char ch = gdg_idx_to_ch(i);
		const uint32_t letter_set = gdg->letter_sets[node];
		const uint32_t next_node = gdg_follow_edge(gdg, node, ch);

		if (i > 0 && (letter_set >> i) & 1) {
			char *word = NULL;

			word = calloc(len + 2, sizeof(char));
			if (word == NULL)
				return NULL;

			if (append) {
				memcpy(word, partial_word, len);
				word[len] = ch;
			} else {
				word[0] = ch;
				memcpy(word + 1, partial_word, len);
			}

			if (res == NULL)
				res = gdg_create_result(word, NULL);
			else
				res = gdg_create_result(word, res);

			free(word);
		}

		if (next_node != 0) {
			if (i == 0)
				res = gdg_crawl(gdg,
				                next_node,
				                partial_word,
				                res,
						false,
				                true);
			else {
				char *new_partial_word = NULL;

				new_partial_word = calloc(len + 2,
				                          sizeof(char));
				if (new_partial_word == NULL)
					return NULL;

				if (append) {
					memcpy(new_partial_word,
					       partial_word,
					       len);
					new_partial_word[len] = ch;
				} else {
					new_partial_word[0] = ch;
					memcpy(new_partial_word + 1,
					       partial_word,
					       len);
				}

				res = gdg_crawl(gdg,
				                next_node,
				                new_partial_word,
				                res,
				                wrap,
				                append);

				free(new_partial_word);
			}
		}
	}

	return res;
}
