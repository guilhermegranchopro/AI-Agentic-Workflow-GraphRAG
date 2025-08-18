// Schema creation for UAE Legal GraphRAG
// Create constraints and indexes

// Unique constraints
CREATE CONSTRAINT instrument_id_unique IF NOT EXISTS FOR (i:Instrument) REQUIRE i.id IS UNIQUE;
CREATE CONSTRAINT provision_id_unique IF NOT EXISTS FOR (p:Provision) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT gazette_id_unique IF NOT EXISTS FOR (g:GazetteIssue) REQUIRE g.id IS UNIQUE;
CREATE CONSTRAINT court_id_unique IF NOT EXISTS FOR (c:Court) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT judgment_id_unique IF NOT EXISTS FOR (j:Judgment) REQUIRE j.id IS UNIQUE;
CREATE CONSTRAINT event_id_unique IF NOT EXISTS FOR (e:Event) REQUIRE e.id IS UNIQUE;

// Fulltext index for provision text search
CREATE FULLTEXT INDEX provision_text_index IF NOT EXISTS FOR (p:Provision) ON EACH [p.text];

// Standard indexes for common queries
CREATE INDEX provision_number_index IF NOT EXISTS FOR (p:Provision) ON (p.number);
CREATE INDEX instrument_type_index IF NOT EXISTS FOR (i:Instrument) ON (i.type);
CREATE INDEX event_valid_from_index IF NOT EXISTS FOR (e:Event) ON (e.valid_from);
CREATE INDEX event_valid_to_index IF NOT EXISTS FOR (e:Event) ON (e.valid_to);
