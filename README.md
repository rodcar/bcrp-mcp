<div align="center">

# BRCP-MCP
#### **Model Context Protocol (MCP) Server for BCRP Economic and Financial Time Series Data**

---

### 👨‍💻 Author

**Ivan Yang Rodriguez Carranza**

[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ivanrodcar@outlook.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/irodcar)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rodcar)

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🔧 Tools](#-tools)
- [💬 Prompts](#-prompts)
- [🚀 How to Use](#-how-to-use)
- [💡 Examples](#-examples)
- [🏛️ Architecture Diagram](#️-architecture-diagram)
- [📝 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

BRCP-MCP is a **Model Context Protocol (MCP) server** that provides seamless access to economic and financial time series data from the **BCRP (Banco Central de Reserva del Perú)** - Peru's Central Reserve Bank. This server enables AI assistants and applications to search, explore, and analyze Peru's economic indicators, financial statistics, and monetary data through a standardized MCP interface.

---

## 🔧 Tools

| Name | Input | Description |
|------|-------|-------------|
| `search_time_series_groups` | `keywords` | Search for time series groups using one or multiple keywords |
| `search_time_series_by_group` | `time_series_group` | Find all time series within a specific group, returns code and name pairs |
| `get_time_series_data` | `time_series_code`<br/>`start`<br/>`end` | Retrieve time series data for a specific code within a date range |

---

## 💬 Prompts

| Name | Input | Description |
|------|-------|-------------|
| `search_data` | `keyword` | Guided workflow to find relevant time series using keyword search |
| `ask` | `question` | Financial analysis workflow that extracts keywords, searches data, and answers questions |

---

## 🚀 How to Use

### **Claude Desktop (Remote Server)**

Add to Claude Desktop config (Claude > Settings > Developer > Edit Config):
   ```json
   ```

### **Local Server**

Clone and install:
   ```bash
   git clone https://github.com/rodcar/brcp-mcp.git
   cd brcp-mcp
   uv sync
   ```

Add to Claude Desktop config (Claude > Settings > Developer > Edit Config):

   > **Note:** Replace `/path/to/brcp-mcp` with the actual path where you cloned the repository.

   ```json
   {
     "mcpServers": {
       "simple_mcp": {
         "command": "uv",
         "args": [
           "--directory",
           "/path/to/brcp-mcp",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```

---

## 💡 Examples

| Prompt | Language | Question | Conversation |
|--------|----------|----------|-------------|
| `ask` | Spanish | "¿Cómo ha evolucionado la tasa de interés de referencia en el último año?" | [https://claude.ai/share/34df5f90-7a35-474d-b4cf-e8f48c3f9772](https://claude.ai/share/34df5f90-7a35-474d-b4cf-e8f48c3f9772) |

---

## 🏛️ Architecture Diagram

BRCP-MCP follows the Model Context Protocol specification and provides a clean abstraction layer over the BCRP API.

```mermaid
graph LR
    CLIENT[MCP Client<br/>Claude Desktop, IDE, etc.] --> MCP_SERVER[BRCP-MCP Server]
    bcrpy --> BCRP_API[BCRP API<br/>estadisticas.bcrp.gob.pe]
    
    subgraph TOOLS ["🔧 Tools"]
        SEARCH_GROUP[search_time_serie_group]
        SEARCH_SERIES[search_time_series_by_group]
        GET_DATA[get_time_series_data]
    end
    
    subgraph "💬 Prompts"
        SEARCH_PROMPT[search_data]
        ASK_PROMPT[ask]
    end
    
    MCP_SERVER --> SEARCH_GROUP
    MCP_SERVER --> SEARCH_SERIES
    MCP_SERVER --> GET_DATA
    MCP_SERVER --> SEARCH_PROMPT
    MCP_SERVER --> ASK_PROMPT
    
    TOOLS --> bcrpy
    TOOLS --> BCRP_API
    
    style CLIENT fill:#e3f2fd
    style MCP_SERVER fill:#f3e5f5
    style bcrpy fill:#e8f5e8
    style BCRP_API fill:#fff3e0
```

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **BCRP** for providing open access to Peru's economic data
- **bcrpy** library for the Python interface to BCRP data

---

<div align="center">

[Report Bug](https://github.com/rodcar/brcp-mcp/issues) · [Request Feature](https://github.com/rodcar/brcp-mcp/issues) · [Documentation](https://github.com/rodcar/brcp-mcp/wiki)

</div>