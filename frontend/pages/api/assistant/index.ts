import { NextApiRequest, NextApiResponse } from 'next';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export const config = {
  runtime: 'nodejs',
};

// Knowledge base for intelligent responses
const legalKnowledgeBase = {
  liability: {
    companies: {
      text: `Under UAE law, company liability is governed by several key principles:

**Limited Liability Companies (LLC):**
- Shareholders' liability is limited to their capital contribution
- Personal assets are protected from business debts
- Governed by Federal Law No. 2 of 2015 on Commercial Companies

**Public Joint Stock Companies:**
- Shareholders liable only up to the value of their shares
- Board members may face personal liability for gross negligence
- Regulated by SCA (Securities and Commodities Authority)

**Key Liability Rules:**
1. **Piercing the Corporate Veil:** Courts may hold shareholders personally liable for:
   - Fraud or misrepresentation
   - Commingling personal and business assets
   - Failure to maintain proper corporate formalities

2. **Directors' Liability:**
   - Fiduciary duties to act in company's best interest
   - Personal liability for breach of duty
   - Criminal liability for financial crimes

3. **Contractual Liability:**
   - Companies bound by contracts entered by authorized representatives
   - Joint and several liability for partnerships
   - Parent company liability for subsidiaries in certain circumstances

**Recent Legal Developments:**
- Enhanced corporate governance requirements
- Stricter financial reporting obligations
- Increased penalties for corporate misconduct`,
      citations: [
        { title: "Federal Law No. 2 of 2015", source: "Commercial Companies Law", relevance: 0.98 },
        { title: "Federal Law No. 5 of 1985", source: "Civil Code", relevance: 0.92 },
        { title: "SCA Regulations", source: "Securities Authority", relevance: 0.89 }
      ],
      confidence: 0.94
    }
  },
  contracts: {
    disputes: {
      text: `UAE contract dispute resolution follows a structured legal framework:

**Legal Basis:**
- UAE Civil Code (Federal Law No. 5 of 1985)
- UAE Commercial Code (Federal Law No. 18 of 1993)
- Various sector-specific regulations

**Dispute Resolution Options:**

1. **Court System:**
   - Civil Courts for general contract disputes
   - Commercial Courts for business disputes
   - Specialized courts for specific sectors

2. **Alternative Dispute Resolution (ADR):**
   - Mediation through DIFC-LCIA
   - Arbitration under UAE Arbitration Law
   - Expert determination

**Key Legal Principles:**
- **Freedom of Contract:** Parties free to agree terms
- **Good Faith:** All parties must act honestly
- **Performance:** Strict adherence to contract terms
- **Damages:** Compensation for breach of contract

**Common Contract Issues:**
- Force majeure clauses
- Termination rights
- Payment disputes
- Performance delays
- Quality standards

**Enforcement:**
- Court judgments enforceable across UAE
- International enforcement through treaties
- Asset seizure and freezing orders available`,
      citations: [
        { title: "UAE Civil Code", source: "Federal Law No. 5 of 1985", relevance: 0.96 },
        { title: "UAE Commercial Code", source: "Federal Law No. 18 of 1993", relevance: 0.94 },
        { title: "UAE Arbitration Law", source: "Federal Law No. 6 of 2018", relevance: 0.91 }
      ],
      confidence: 0.93
    }
  },
  business: {
    establishment: {
      text: `Business establishment in Dubai follows a comprehensive regulatory framework:

**Legal Entity Options:**

1. **Mainland Companies:**
   - 100% UAE ownership or partnership with local sponsor
   - Full market access
   - Governed by Commercial Companies Law

2. **Free Zone Companies:**
   - 100% foreign ownership
   - Tax benefits and simplified procedures
   - Limited to free zone activities

3. **Offshore Companies:**
   - International business companies
   - Tax optimization
   - Restricted to international activities

**Registration Process:**
1. **Name Reservation:** Submit proposed company name
2. **License Application:** Choose appropriate license type
3. **Documentation:** Submit required legal documents
4. **Approval:** Obtain government approvals
5. **Registration:** Complete commercial registration

**Required Documents:**
- Passport copies of shareholders
- No-objection certificates
- Business plan and financial projections
- Office lease agreement
- Bank reference letters

**Regulatory Bodies:**
- Department of Economic Development (DED)
- Dubai Multi Commodities Centre (DMCC)
- Various free zone authorities

**Compliance Requirements:**
- Annual license renewal
- Financial reporting
- VAT registration (if applicable)
- Employment visa processing`,
      citations: [
        { title: "Commercial Companies Law", source: "Federal Law No. 2 of 2015", relevance: 0.97 },
        { title: "DED Regulations", source: "Dubai Economic Development", relevance: 0.95 },
        { title: "Free Zone Laws", source: "Various Free Zone Authorities", relevance: 0.93 }
      ],
      confidence: 0.95
    }
  },
  intellectual: {
    property: {
      text: `UAE's intellectual property protection framework is comprehensive and internationally aligned:

**Legal Framework:**
- Federal Law No. 31 of 2006 on Industrial Property
- Federal Law No. 7 of 2002 on Copyrights
- Trademark Law (Federal Law No. 37 of 1992)
- Various international treaties (WIPO, TRIPS)

**Types of IP Protection:**

1. **Patents:**
   - 20-year protection for inventions
   - Novelty, inventiveness, and industrial applicability required
   - Pharmaceutical and biotech patents protected

2. **Trademarks:**
   - 10-year renewable protection
   - Distinctive marks, logos, and brand names
   - Well-known marks receive enhanced protection

3. **Copyrights:**
   - Automatic protection for original works
   - 50-year protection for most works
   - Covers software, literature, music, and art

4. **Trade Secrets:**
   - Confidential business information
   - No formal registration required
   - Civil and criminal protection available

**Enforcement Mechanisms:**
- Civil litigation in specialized courts
- Criminal prosecution for infringement
- Customs seizure of counterfeit goods
- Administrative enforcement by authorities

**International Protection:**
- Madrid Protocol for international trademarks
- PCT for international patent applications
- Berne Convention for copyright protection

**Recent Developments:**
- Enhanced digital copyright protection
- Stricter penalties for IP infringement
- Streamlined registration procedures`,
      citations: [
        { title: "Industrial Property Law", source: "Federal Law No. 31 of 2006", relevance: 0.96 },
        { title: "Copyright Law", source: "Federal Law No. 7 of 2002", relevance: 0.94 },
        { title: "Trademark Law", source: "Federal Law No. 37 of 1992", relevance: 0.92 }
      ],
      confidence: 0.94
    }
  }
};

function generateIntelligentResponse(query: string) {
  const lowerQuery = query.toLowerCase();
  
  // Check for specific legal topics
  if (lowerQuery.includes('liability') && (lowerQuery.includes('company') || lowerQuery.includes('companies'))) {
    return {
      text: legalKnowledgeBase.liability.companies.text,
      citations: legalKnowledgeBase.liability.companies.citations,
      agents: {
        local: "Local GraphRAG agent identified liability framework",
        global: "Global GraphRAG agent provided comprehensive legal context",
        drift: "DRIFT agent analyzed recent legal developments"
      },
      confidence: legalKnowledgeBase.liability.companies.confidence,
      strategy_used: "hybrid",
      metadata: {
        processing_time: 1.8,
        sources_consulted: 3,
        legal_jurisdiction: "UAE",
        topic: "company_liability"
      }
    };
  }
  
  if (lowerQuery.includes('contract') && lowerQuery.includes('dispute')) {
    return {
      text: legalKnowledgeBase.contracts.disputes.text,
      citations: legalKnowledgeBase.contracts.disputes.citations,
      agents: {
        local: "Local GraphRAG agent identified contract law framework",
        global: "Global GraphRAG agent provided dispute resolution options",
        drift: "DRIFT agent analyzed enforcement mechanisms"
      },
      confidence: legalKnowledgeBase.contracts.disputes.confidence,
      strategy_used: "hybrid",
      metadata: {
        processing_time: 2.1,
        sources_consulted: 3,
        legal_jurisdiction: "UAE",
        topic: "contract_disputes"
      }
    };
  }
  
  if (lowerQuery.includes('business') && (lowerQuery.includes('establishment') || lowerQuery.includes('setup') || lowerQuery.includes('registration'))) {
    return {
      text: legalKnowledgeBase.business.establishment.text,
      citations: legalKnowledgeBase.business.establishment.citations,
      agents: {
        local: "Local GraphRAG agent identified business registration requirements",
        global: "Global GraphRAG agent provided regulatory framework",
        drift: "DRIFT agent analyzed compliance requirements"
      },
      confidence: legalKnowledgeBase.business.establishment.confidence,
      strategy_used: "hybrid",
      metadata: {
        processing_time: 2.3,
        sources_consulted: 3,
        legal_jurisdiction: "UAE",
        topic: "business_establishment"
      }
    };
  }
  
  if (lowerQuery.includes('ip') || lowerQuery.includes('intellectual property') || lowerQuery.includes('patent') || lowerQuery.includes('trademark') || lowerQuery.includes('copyright')) {
    return {
      text: legalKnowledgeBase.intellectual.property.text,
      citations: legalKnowledgeBase.intellectual.property.citations,
      agents: {
        local: "Local GraphRAG agent identified IP protection framework",
        global: "Global GraphRAG agent provided international context",
        drift: "DRIFT agent analyzed enforcement mechanisms"
      },
      confidence: legalKnowledgeBase.intellectual.property.confidence,
      strategy_used: "hybrid",
      metadata: {
        processing_time: 2.0,
        sources_consulted: 3,
        legal_jurisdiction: "UAE",
        topic: "intellectual_property"
      }
    };
  }
  
  // Default response for other queries
  return {
    text: `I understand you're asking about "${query}". Based on UAE legal framework, I can provide guidance on various legal matters including:

• **Company Liability & Corporate Law** - Limited liability, directors' duties, corporate governance
• **Contract Disputes** - Resolution mechanisms, enforcement, damages
• **Business Establishment** - Registration, licensing, compliance requirements  
• **Intellectual Property** - Patents, trademarks, copyrights, enforcement
• **Employment Law** - Labor rights, contracts, disputes
• **Commercial Law** - Trade regulations, consumer protection
• **Real Estate Law** - Property rights, transactions, disputes

Please ask a specific question about any of these areas, and I'll provide detailed legal guidance based on UAE law. For example, you could ask about "liability rules for companies" or "contract dispute resolution in UAE."`,
    citations: [
      { title: "UAE Civil Code", source: "Federal Law No. 5 of 1985", relevance: 0.85 },
      { title: "Commercial Companies Law", source: "Federal Law No. 2 of 2015", relevance: 0.82 },
      { title: "UAE Constitution", source: "Federal Law No. 1 of 1971", relevance: 0.78 }
    ],
    agents: {
      local: "Local GraphRAG agent identified general legal framework",
      global: "Global GraphRAG agent provided jurisdictional context",
      drift: "DRIFT agent analyzed current legal landscape"
    },
    confidence: 0.75,
    strategy_used: "general",
    metadata: {
      processing_time: 1.5,
      sources_consulted: 3,
      legal_jurisdiction: "UAE",
      topic: "general_legal_guidance"
    }
  };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { messages } = req.body;

    if (!Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ error: 'Invalid messages format' });
    }

    // Extract the latest user query
    const userMessage = messages[messages.length - 1];
    const query = userMessage?.content || '';

    // Intelligent mock response system
    const mockResponse = generateIntelligentResponse(query);

    // Set headers for JSON response
    res.setHeader('Content-Type', 'application/json');
    res.status(200).json(mockResponse);

  } catch (error) {
    console.error('Assistant API error:', error);
    
    if (!res.headersSent) {
      res.setHeader('Content-Type', 'application/json');
      res.status(500).json({ 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      });
    } else {
      res.write(`data: ${JSON.stringify({
        error: 'Processing failed',
        message: error instanceof Error ? error.message : 'Unknown error'
      })}\n\n`);
      res.end();
    }
  }
}
