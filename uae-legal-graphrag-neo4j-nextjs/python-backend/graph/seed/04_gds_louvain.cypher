// GDS Louvain community detection
// Project graph with provisions and judgments, connected by citations and interpretations

CALL gds.graph.project(
    'legal-network',
    ['Provision', 'Judgment'],
    {
        CITES: {
            orientation: 'UNDIRECTED'
        },
        INTERPRETED_BY: {
            orientation: 'UNDIRECTED'
        },
        INTERPRETS: {
            orientation: 'UNDIRECTED'
        }
    }
);

// Run Louvain community detection
CALL gds.louvain.mutate(
    'legal-network',
    {
        mutateProperty: 'communityId',
        includeIntermediateCommunities: false
    }
);

// Write community IDs back to nodes
CALL gds.graph.nodeProperties.write(
    'legal-network',
    ['communityId']
);

// Drop the projected graph
CALL gds.graph.drop('legal-network');
