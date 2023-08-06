#ifndef GADDAG_H_INCLUDED
#define GADDAG_H_INCLUDED

#include <stdbool.h>
#include <stdint.h>


extern const uint32_t GDG_CAP;
extern const uint32_t GDG_MAX_CHARS;

typedef struct GADDAG_Struct GADDAG;
typedef struct Result_Struct Result;

/**
 * A GADDAG.
 */
struct GADDAG_Struct {
	uint32_t cap;
	uint32_t num_words;
	uint32_t num_nodes;
	uint32_t num_edges;
	uint32_t *edges;
	uint32_t *letter_sets;
};

/**
 * Doubly-linked list used to return words found in the GADDAG.
 */
struct Result_Struct {
	const char* str;
	Result *next;
	Result *prev;
};

/**
 * \brief Creates a new GADDAG.
 *
 * Allocates a new GADDAG structure on the heap and initialises its fields.
 *
 * \return Newly created GADDAG.
 *
 * \retval NULL Failed to allocate memory for GADDAG.
 */
GADDAG* gdg_create(void);

/**
 * \brief Save an uncompressed GADDAG to a file.
 *
 * Saves a GADDAG to a file without compression. This can be hundreds of
 * megabytes!
 *
 * \param gdg GADDAG to save.
 * \param path Path to save GADDAG as a file.
 *
 * \return Total bytes written to file.
 *
 * \retval -1 Failed to open file for writing.
 */
off_t gdg_save(const GADDAG *gdg, const char *path);

#ifdef COMPRESSION
/**
 * \brief Save a compressed GADDAG to a file.
 *
 * Saves a GADDAG to a file with compression. This can be 1-2 orders of
 * magnitude smaller than an uncompressed GADDAG.
 *
 * \param gdg GADDAG to save.
 * \param path Path to save GADDAG as a file.
 *
 * \return Total (uncompressed) bytes written to file.
 *
 * \retval -1 Failed to open file for writing.
 */
off_t gdg_save_compressed(const GADDAG *gdg, const char *path);
#endif

/**
 * \brief Load a GADDAG from file.
 *
 * Load a GADDAG from a file, regardless of whether it is compressed or not.
 * It will take longer to load a compressed GADDAG as it must be uncompressed
 * into memory.
 *
 * \param path Path to saved GADDAG to load.
 *
 * \return Loaded GADDAG.
 *
 * \retval NULL Failed to allocate memory for GADDAG, or open file for reading.
 */
GADDAG* gdg_load(const char *path);

/**
 * \brief Destroy a GADDAG.
 *
 * Release the resources allocated to a GADDAG. The GADDAG will be unusable
 * after being destroyed.
 *
 * \param gdg GADDAG to destroy.
 */
void gdg_destroy(GADDAG *gdg);

/**
 * \brief Add a word to a GADDAG.
 *
 * Add the necessary edge(s), node(s) and letter set(s) required to describe a
 * word to a GADDAG. The word _must_ contain only ASCII characters [A-Za-z].
 *
 * \param gdg GADDAG to add word to.
 * \param word Word to add to the GADDAG.
 *
 * \return Integer indicating success/failure.
 *
 * \retval 0 Word was successfully added.
 * \retval 1 The word contains non-ASCII characters.
 * \retval 2 Word could not be added due to running out of memory, this leaves
 *           the GADDAG in an undefined state.
 */
int gdg_add_word(GADDAG *gdg, const char *word);

/**
 * \brief Check if a word is in a GADDAG.
 *
 * Traverse the GADDAG, following the characters of the word in reverse, to
 * check if the GADDAG contains the word.
 *
 * \param gdg GADDAG to search.
 * \param word Word to search for.
 *
 * \return Boolean indicating whether the word is in the GADDAG or not.
 *
 * \retval true Word is present.
 * \retval false Word is not present.
 */
bool gdg_has(const GADDAG *gdg, const char *word);

/**
 * \brief Get all words in a GADDAG which start with a prefix.
 *
 * Traverse the GADDAG, following the characters of the word in reverse and
 * the break edge ('+') before crawling every edge to find all the
 * words starting with a prefix.
 *
 * \param gdg GADDAG to search.
 * \param prefix Prefix to search for.
 *
 * \return Doubly-linked list of found words.
 *
 * \retval NULL The prefix itself was not in the GADDAG, or no words start with
 *              the prefix.
 */
Result* gdg_starts_with(const GADDAG *gdg, const char *prefix);

/**
 * \brief Get all words in a GADDAG which contain a substring.
 *
 * Traverse the GADDAG, following the characters of the word in reverse before
 * crawling every edge to find all the words containing a substring.
 *
 * \param gdg GADDAG to search.
 * \param sub Substring to search for.
 *
 * \return Doubly-linked list of found words.
 *
 * \retval NULL The substring itself was not in the GADDAG, or no words contain
 *              the substring.
 */
Result* gdg_contains(const GADDAG *gdg, const char *sub);

/**
 * \brief Get all words in a GADDAG which end with a suffix.
 *
 * Traverse the GADDAG, following the characters of the word in reverse before
 * crawling every edge except the break edge ('+') to find all the words
 * containing a substring.
 *
 * \param gdg GADDAG to search.
 * \param suffix Suffix to search for.
 *
 * \return Doubly-linked list of found words.
 *
 * \retval NULL The suffix itself was not in the GADDAG, or no words end with
 *              the suffix.
 */
Result* gdg_ends_with(const GADDAG *gdg, const char *suffix);

/**
 * \brief Retrieve all the edges of a node.
 *
 * Retrieve all edges _from_ a node and place them into a buffer. To just count
 * the edges, provide NULL for the buffer. A node may have up to
 * `27` edges.
 *
 * \param gdg GADDAG node belongs to.
 * \param node Node to retrieve edges of.
 * \param buf Buffer to place retrieved edges in. Can be NULL.
 *
 * \return Number of edges from the provided node.
 */
int gdg_edges(const GADDAG *gdg, const uint32_t node, char *buf);

/**
 * \brief Retrieve the letter set of a node.
 *
 * Retrieve the letter set of a node and place it into a buffer. To just count
 * the characters in the letter set, provide NULL for the buffer. A node may
 * have up to `27` characters in its letter set.
 *
 * \param gdg GADDAG node belongs to.
 * \param node Node to retrieve letter set of.
 * \param buf Buffer to place retrieved letter set in. Can be NULL.
 *
 * \return Number of characters in the letter set of the provided node.
 */
int gdg_letter_set(const GADDAG *gdg, const uint32_t node, char *buf);

/**
 * \brief Check if a character is the end of a word.
 *
 * Checks if a character is part of a node's letter set.
 *
 * \param gdg GADDAG node belongs to.
 * \param node Node to check letter set of.
 * \param ch Character to check for in the letter set.
 *
 * \return True if the letter set contains the character, false otherwise.
 */
bool gdg_is_end(const GADDAG *gdg, const uint32_t node, const char ch);

/**
 * \brief Follow an edge from a node.
 *
 * Attempt to traverse an edge from a node in a GADDAG to find a new node.
 *
 * \param gdg GADDAG node belongs to.
 * \param node Node to follow edge of.
 * \param ch Edge to follow.
 *
 * \return New node index found by following edge. 
 *
 * \retval 0 No such edge exists.
 */
uint32_t gdg_follow_edge(const GADDAG *gdg, const uint32_t node, const char ch);

/**
 * \brief Destroy a doubly-linked Result list.
 *
 * Release the resources allocated to a doubly-linked Result list. Every Result
 * in the list, whether before or after the provided Result, will be destroyed.
 * The Result(s) will be unusable after being destroyed.
 *
 * \param res Result list to destroy.
 */
void gdg_destroy_result(Result *res);
#endif

