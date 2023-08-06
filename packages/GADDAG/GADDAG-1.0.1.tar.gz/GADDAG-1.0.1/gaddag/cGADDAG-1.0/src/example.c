#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <err.h>

#include "cgaddag.h"

int
main(void)
{
	GADDAG *gdg = NULL;
	Result *res = NULL;
	Result *tmp = NULL;
	uint32_t r_node;
	uint32_t ra_node;
	char edge_letters[GDG_MAX_CHARS];
	char end_letters[GDG_MAX_CHARS];
	off_t size;

	if ((gdg = gdg_create()) == NULL)
		errx(1, "Failed to allocate a new GADDAG");
	printf("Created a new GADDAG\n");

	if (gdg_add_word(gdg, "CARE") != 0)
		errx(1, "Failed to add \"CARE\" to GADDAG");
	printf("Added \"CARE\" to GADDAG\n");

	if (gdg_add_word(gdg, "CAR") != 0)
		errx(1, "Failed to add \"CAR\" to GADDAG");
	printf("Added \"CAR\" to GADDAG\n");

	if (gdg_add_word(gdg, "BAR") != 0)
		errx(1, "Failed to add \"BAR\" to GADDAG");
	printf("Added \"BAR\" to GADDAG\n");

	printf("\nNode capacity: %u\n", gdg->cap);
	printf("Total words: %u\n", gdg->num_words);
	printf("Total nodes: %u\n", gdg->num_nodes);
	printf("Total edges: %u\n", gdg->num_edges);

	printf("\nContains CARE: %d\n", gdg_has(gdg, "CARE"));
	printf("Contains CAR: %d\n", gdg_has(gdg, "CAR"));
	printf("Contains FOO: %d\n", gdg_has(gdg, "FOO"));

	printf("\nFinding words ending with 'AR'\n");
	res = gdg_ends_with(gdg, "ar");
	if (res) {
		tmp = res;
		while (tmp != NULL) {
			printf("  %s\n", tmp->str);
			tmp = tmp->next;
		}
		gdg_destroy_result(res);
	} else
		printf("  No words found\n");

	printf("\nFinding words starting with 'CAR'\n");
	res = gdg_starts_with(gdg, "car");
	if (res) {
		tmp = res;
		while (tmp) {
			printf("  %s\n", tmp->str);
			tmp = tmp->next;
		}
		gdg_destroy_result(res);
	} else
		printf("  No words found\n");

	printf("\nFinding words containing 'AR'\n");
	res = gdg_contains(gdg, "ar");
	if (res) {
		tmp = res;
		while (tmp) {
			printf("  %s\n", tmp->str);
			tmp = tmp->next;
		}
		gdg_destroy_result(res);
	} else
		printf("  No words found\n");

	r_node = gdg_follow_edge(gdg, 0, 'R');
	ra_node = gdg_follow_edge(gdg, r_node, 'A');

	memset(edge_letters, '\0', GDG_MAX_CHARS);
	printf("\nEdges from root (%u): %s\n",
	       gdg_edges(gdg, 0, edge_letters),
	       edge_letters);

	memset(end_letters, '\0', GDG_MAX_CHARS);
	printf("Letter set for root -> R -> A (%u): %s\n",
	       gdg_letter_set(gdg, ra_node, end_letters),
	       end_letters);

	printf("\nSaving GADDAG to 'example.gdg': ");
	size = gdg_save(gdg, "example.gdg");
	printf("%lld\n", (long long)size);

#ifdef COMPRESSION
	printf("Saving compressed GADDAG to 'example.gdg.gz': ");
	size = gdg_save_compressed(gdg, "example.gdg.gz");
	printf("%lld\n", (long long)size);
#endif

	gdg_destroy(gdg);
}

