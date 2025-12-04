# AI Crew Org Charts

Visual representations of the agent hierarchy and relationships.

---

## Mermaid Diagram: Full Hierarchy

```mermaid
flowchart TB
    subgraph Principal
        JD[("JD<br/>Principal")]
    end

    subgraph Coordination["Coordination Layer"]
        Xavier["Xavier<br/>Chief of Staff"]
        Aurelius["Aurelius<br/>Keeper of Charter"]
        Clare["Clare<br/>Communications"]
    end

    subgraph Personal["Personal Staff"]
        Evelyn["Evelyn<br/>Exec Assistant"]
        Eleanor["Eleanor<br/>Relationship Steward"]
        Warren["Warren<br/>Finance"]
        Hetty["Hetty<br/>Tax"]
        Galen["Galen<br/>Health"]
        Martha["Martha<br/>Household"]
        Marco["Marco<br/>Travel"]
        Seneca["Seneca<br/>Learning"]
        Iris["Iris<br/>Knowledge"]
    end

    subgraph HazeGray["Haze Gray Consulting"]
        Helena["Helena<br/>BD Manager"]
        Cicero["Cicero<br/>Persuasion"]
        Dale["Dale<br/>Content"]
        Hamilton["Hamilton<br/>Engagement"]
    end

    subgraph Puzzlehouse["Puzzlehouse.com"]
        Ada["Ada<br/>Social Media"]
        Franklin["Franklin<br/>Store Ops"]
        Clara["Clara<br/>Customer Svc"]
    end

    %% Principal to Coordination
    JD --> Xavier
    JD --> Aurelius
    JD --> Clare

    %% Xavier to Domains
    Xavier --> Personal
    Xavier --> HazeGray
    Xavier --> Puzzlehouse

    %% Supervisor relationships
    Warren --> Hetty
    Franklin --> Clara

    %% Content flow
    Dale -.->|content| Clare

    %% Cross-domain coordination
    Ada -.->|inventory| Franklin
    Helena -.->|leads| Cicero
    Helena -.->|CRM data| Eleanor
    Dale -.->|engagement| Helena

    %% Escalation paths
    Personal -.->|escalations| Aurelius
    HazeGray -.->|escalations| Aurelius
    Puzzlehouse -.->|escalations| Aurelius

    %% Briefing flow
    Personal -.->|reports| Clare
    HazeGray -.->|reports| Clare
    Puzzlehouse -.->|reports| Clare
```

---

## Mermaid Diagram: Reporting Hierarchy Only

```mermaid
flowchart TB
    JD(["JD"])

    JD --> Xavier["Xavier"]
    JD --> Aurelius["Aurelius"]
    JD --> Clare["Clare"]

    Xavier --> Evelyn["Evelyn"]
    Xavier --> Eleanor["Eleanor"]
    Xavier --> Warren["Warren"]
    Xavier --> Galen["Galen"]
    Xavier --> Martha["Martha"]
    Xavier --> Marco["Marco"]
    Xavier --> Seneca["Seneca"]
    Xavier --> Iris["Iris"]
    Xavier --> Helena["Helena"]
    Xavier --> Cicero["Cicero"]
    Xavier --> Dale["Dale"]
    Xavier --> Hamilton["Hamilton"]
    Xavier --> Ada["Ada"]
    Xavier --> Franklin["Franklin"]

    Warren --> Hetty["Hetty"]
    Franklin --> Clara["Clara"]
```

---

## Mermaid Diagram: Information Flows

```mermaid
flowchart LR
    subgraph Input["Inputs"]
        Email["Email"]
        Calendar["Calendar"]
        Shopify["Shopify"]
        Social["Social Platforms"]
        Financial["Financial Data"]
    end

    subgraph Agents["Agent Processing"]
        Evelyn["Evelyn"]
        Ada["Ada"]
        Franklin["Franklin"]
        Warren["Warren"]
        Dale["Dale"]
    end

    subgraph Coordination["Coordination"]
        Xavier["Xavier"]
        Clare["Clare"]
    end

    subgraph Output["Outputs"]
        Briefing["Morning Briefing"]
        Actions["Automated Actions"]
        Alerts["Exception Alerts"]
        Reports["Weekly Reports"]
    end

    Email --> Evelyn
    Calendar --> Evelyn
    Shopify --> Franklin
    Shopify --> Ada
    Social --> Ada
    Financial --> Warren

    Evelyn --> Xavier
    Ada --> Xavier
    Franklin --> Xavier
    Warren --> Xavier
    Dale --> Xavier

    Xavier --> Clare
    Clare --> Briefing
    Clare --> Reports

    Evelyn --> Actions
    Ada --> Actions
    Franklin --> Actions

    Xavier --> Alerts
```

---

## Mermaid Diagram: Domain Clusters

```mermaid
flowchart TB
    subgraph Coordination["🎯 Coordination Layer"]
        direction LR
        Xavier["Xavier<br/>Operations"]
        Aurelius["Aurelius<br/>Accountability"]
        Clare["Clare<br/>Communications"]
    end

    subgraph Personal["👤 Personal Staff"]
        direction TB
        Evelyn["Evelyn - EA"]
        Eleanor["Eleanor - CRM"]
        Warren["Warren - Finance"]
        Hetty["Hetty - Tax"]
        Galen["Galen - Health"]
        Martha["Martha - Home"]
        Marco["Marco - Travel"]
        Seneca["Seneca - Learning"]
        Iris["Iris - Knowledge"]
    end

    subgraph HazeGray["💼 Haze Gray"]
        direction TB
        Helena["Helena - BD"]
        Cicero["Cicero - Pitches"]
        Dale["Dale - Content"]
        Hamilton["Hamilton - Delivery"]
    end

    subgraph Puzzlehouse["🧩 Puzzlehouse"]
        direction TB
        Ada["Ada - Social"]
        Franklin["Franklin - Ops"]
        Clara["Clara - Support"]
    end

    Coordination --> Personal
    Coordination --> HazeGray
    Coordination --> Puzzlehouse
```

---

## Mermaid Diagram: Escalation Paths

```mermaid
flowchart BT
    subgraph Level4["Level 4: Principal"]
        JD(["JD"])
    end

    subgraph Level3["Level 3: Coordination"]
        Xavier["Xavier<br/>Operational Issues"]
        Aurelius["Aurelius<br/>Values Issues"]
        Clare["Clare<br/>Comms Issues"]
    end

    subgraph Level2["Level 2: Supervisors"]
        Warren["Warren<br/>Finance Domain"]
        Franklin["Franklin<br/>Puzzlehouse Domain"]
    end

    subgraph Level1["Level 1: Agents"]
        Hetty["Hetty"]
        Clara["Clara"]
        Others["All Other Agents"]
    end

    Hetty -->|tax matters| Warren
    Clara -->|customer issues| Franklin
    Warren -->|financial escalations| Xavier
    Franklin -->|operational escalations| Xavier
    Others -->|operational| Xavier
    Others -->|values/ethics| Aurelius
    Others -->|communication| Clare
    Xavier --> JD
    Aurelius --> JD
    Clare --> JD
```

---

## How to Use These Diagrams

### In GitHub
GitHub renders Mermaid automatically. Just view this file.

### In Notion
Copy the Mermaid code block and paste into a Notion code block with language set to "mermaid".

### In Obsidian
Mermaid is natively supported. Just paste.

### Export to PNG/SVG
Use the [Mermaid Live Editor](https://mermaid.live):
1. Paste the diagram code
2. Click "Download PNG" or "Download SVG"

### In Presentations
Export as image, or use tools like [Mermaid Chart](https://www.mermaidchart.com/) for interactive versions.

---

## Excalidraw Version

For a more free-form visual, see [ORG_CHART.excalidraw](ORG_CHART.excalidraw).

The Excalidraw file provides:
- Drag-and-drop repositioning
- Hand-drawn aesthetic
- Custom annotations
- Export to PNG, SVG, or embed

---

*Keep these diagrams updated as agents are added or removed.*
