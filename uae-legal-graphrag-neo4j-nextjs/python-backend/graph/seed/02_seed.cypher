// Seed data for UAE Legal GraphRAG demo
// Minimal UAE-ish sample data

// Create Instruments
CREATE (i1:Instrument {
  id: "uae-const-1971",
  title: "Constitution of the United Arab Emirates",
  type: "Constitution",
  year: 1971,
  jurisdiction: "UAE"
});

CREATE (i2:Instrument {
  id: "civil-code-1985",
  title: "UAE Civil Code",
  type: "Federal Law",
  number: "5",
  year: 1985,
  jurisdiction: "UAE"
});

CREATE (i3:Instrument {
  id: "decree-law-2023-3",
  title: "Decree Law on Commercial Companies",
  type: "Decree Law",
  number: "3",
  year: 2023,
  jurisdiction: "UAE"
});

// Create Provisions
CREATE (p1:Provision {
  id: "const-art-12",
  number: "12",
  text: "The Union shall have sovereignty over all land, sea and air territory within its international boundaries.",
  article_title: "Sovereignty",
  instrument_id: "uae-const-1971"
});

CREATE (p2:Provision {
  id: "civil-art-106",
  number: "106", 
  text: "Every person who, without lawful justification, causes damage to another shall be liable to compensate for such damage.",
  article_title: "Civil Liability",
  instrument_id: "civil-code-1985"
});

CREATE (p3:Provision {
  id: "civil-art-264",
  number: "264",
  text: "A contract is concluded by the expression of two concordant intentions without prejudice to what the law provides in addition thereto.",
  article_title: "Contract Formation", 
  instrument_id: "civil-code-1985"
});

CREATE (p4:Provision {
  id: "decree-art-15",
  number: "15",
  text: "Limited liability companies shall have a legal personality separate from that of their shareholders.",
  article_title: "Corporate Personality",
  instrument_id: "decree-law-2023-3"
});

// Create Gazette Issues
CREATE (g1:GazetteIssue {
  id: "gazette-1971-01",
  number: "1",
  date: date("1971-12-02"),
  year: 1971
});

CREATE (g2:GazetteIssue {
  id: "gazette-1985-15",
  number: "15", 
  date: date("1985-09-28"),
  year: 1985
});

CREATE (g3:GazetteIssue {
  id: "gazette-2023-25",
  number: "25",
  date: date("2023-06-15"),
  year: 2023
});

// Create Courts
CREATE (c1:Court {
  id: "difc-courts",
  name: "DIFC Courts",
  jurisdiction: "DIFC",
  type: "Commercial"
});

// Create Judgments
CREATE (j1:Judgment {
  id: "difc-2024-cc-12",
  case_number: "DIFC-2024-CC-12",
  date: date("2024-11-01"),
  court_id: "difc-courts",
  summary: "Interpretation of civil liability principles in commercial context"
});

// Create Events (bi-temporal)
CREATE (e1:Event {
  id: "amend-civil-106-2023",
  kind: "AMENDS",
  description: "Amendment to Article 106 of Civil Code",
  valid_from: date("2023-06-10"),
  valid_to: date("2025-12-31"),
  tx_from: datetime("2023-06-01T10:00:00Z"),
  tx_to: datetime("9999-12-31T23:59:59Z"),
  gazette_ref: "gazette-2023-25"
});

// Create relationships
// Instruments have provisions
MATCH (i1:Instrument {id: "uae-const-1971"}), (p1:Provision {id: "const-art-12"})
CREATE (i1)-[:HAS_PROVISION]->(p1);

MATCH (i2:Instrument {id: "civil-code-1985"}), (p2:Provision {id: "civil-art-106"})
CREATE (i2)-[:HAS_PROVISION]->(p2);

MATCH (i2:Instrument {id: "civil-code-1985"}), (p3:Provision {id: "civil-art-264"})
CREATE (i2)-[:HAS_PROVISION]->(p3);

MATCH (i3:Instrument {id: "decree-law-2023-3"}), (p4:Provision {id: "decree-art-15"})
CREATE (i3)-[:HAS_PROVISION]->(p4);

// Published in gazette
MATCH (i1:Instrument {id: "uae-const-1971"}), (g1:GazetteIssue {id: "gazette-1971-01"})
CREATE (i1)-[:PUBLISHED_IN]->(g1);

MATCH (i2:Instrument {id: "civil-code-1985"}), (g2:GazetteIssue {id: "gazette-1985-15"})
CREATE (i2)-[:PUBLISHED_IN]->(g2);

MATCH (i3:Instrument {id: "decree-law-2023-3"}), (g3:GazetteIssue {id: "gazette-2023-25"})
CREATE (i3)-[:PUBLISHED_IN]->(g3);

// Jurisdiction relationships
MATCH (i2:Instrument {id: "civil-code-1985"}), (i1:Instrument {id: "uae-const-1971"})
CREATE (i2)-[:APPLIES_IN {jurisdiction: "UAE"}]->(i1);

MATCH (i3:Instrument {id: "decree-law-2023-3"}), (i1:Instrument {id: "uae-const-1971"})
CREATE (i3)-[:APPLIES_IN {jurisdiction: "UAE"}]->(i1);

// Amendment event relationships
MATCH (e1:Event {id: "amend-civil-106-2023"}), (p2:Provision {id: "civil-art-106"})
CREATE (e1)-[:AFFECTS]->(p2);

MATCH (p4:Provision {id: "decree-art-15"}), (e1:Event {id: "amend-civil-106-2023"})
CREATE (p4)-[:AMENDED_BY]->(e1);

// Citation relationships
MATCH (p4:Provision {id: "decree-art-15"}), (p2:Provision {id: "civil-art-106"})
CREATE (p4)-[:CITES]->(p2);

MATCH (p3:Provision {id: "civil-art-264"}), (p1:Provision {id: "const-art-12"})
CREATE (p3)-[:CITES]->(p1);

// Judgment relationships
MATCH (j1:Judgment {id: "difc-2024-cc-12"}), (p2:Provision {id: "civil-art-106"})
CREATE (j1)-[:INTERPRETS]->(p2);

MATCH (p2:Provision {id: "civil-art-106"}), (j1:Judgment {id: "difc-2024-cc-12"})
CREATE (p2)-[:INTERPRETED_BY]->(j1);

MATCH (j1:Judgment {id: "difc-2024-cc-12"}), (c1:Court {id: "difc-courts"})
CREATE (j1)-[:ISSUED_BY]->(c1);
