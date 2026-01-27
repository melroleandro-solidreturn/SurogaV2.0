Com base na análise do projeto Django fornecido, aqui está uma especificação JSON detalhada da API implementada:

```json
{
  "api_specification": {
    "project_name": "SurogaAPI / Green Connections API",
    "version": "1.0.0",
    "base_url": "https://api.greenconnections.eu",
    "authentication": {
      "methods": [
        {
          "type": "Token Authentication",
          "header": "Authorization: Token {token}",
          "endpoints_using": [
            "core/*",
            "rides/*"
          ]
        },
        {
          "type": "Session Authentication",
          "endpoints_using": [
            "partner/*",
            "admin/*"
          ]
        }
      ]
    },
    "api_structure": {
      "core": {
        "description": "API core para funcionalidades básicas e dados de referência",
        "base_path": "/api/v1/",
        "endpoints": [
          {
            "path": "/api/v1/time_zones/",
            "methods": ["GET"],
            "description": "Lista fusos horários disponíveis",
            "authentication_required": true,
            "response_model": "time_zone",
            "fields": ["id", "Name", "TimeZone", "UTCoffset"]
          },
          {
            "path": "/api/v1/duration/",
            "methods": ["GET"],
            "description": "Lista durações de passeio disponíveis",
            "authentication_required": true,
            "response_model": "RideDuration",
            "fields": ["id", "Duration"]
          },
          {
            "path": "/api/v1/country/",
            "methods": ["GET"],
            "description": "Lista países disponíveis",
            "authentication_required": true,
            "response_model": "country",
            "fields": ["id", "Name", "Currency", "Language", "PhoneCode", "time_zone", "VAT", "GPS_latitude", "GPS_longitude", "ZoomLevel", "GoogleCode"]
          },
          {
            "path": "/api/v1/currency/",
            "methods": ["GET"],
            "description": "Lista moedas disponíveis",
            "authentication_required": true,
            "response_model": "Currency",
            "fields": ["id", "Name", "Currency", "CurrencySymbol", "SymbolRight"]
          },
          {
            "path": "/api/v1/language/",
            "methods": ["GET"],
            "description": "Lista idiomas disponíveis",
            "authentication_required": true,
            "response_model": "Language",
            "fields": ["id", "Name", "Code"]
          },
          {
            "path": "/api/v1/district_region/",
            "methods": ["GET"],
            "description": "Lista distritos/regiões",
            "authentication_required": true,
            "response_model": "districtregion",
            "fields": ["id", "Name", "GPS_latitude", "GPS_longitude", "ZoomLevel", "GoogleCode"]
          },
          {
            "path": "/api/v1/city_municipality/",
            "methods": ["GET"],
            "description": "Lista cidades/municípios",
            "authentication_required": true,
            "response_model": "citymunicipality",
            "fields": ["id", "Name", "districtregion", "GPS_latitude", "GPS_longitude", "ZoomLevel", "GoogleCode"]
          },
          {
            "path": "/api/v1/equipment/",
            "methods": ["GET"],
            "description": "Lista equipamentos disponíveis",
            "authentication_required": true,
            "response_model": "equipment",
            "fields": ["id", "Name"]
          },
          {
            "path": "/api/v1/public_event/",
            "methods": ["GET"],
            "description": "Lista tipos de eventos públicos",
            "authentication_required": true,
            "response_model": "publicevent",
            "fields": ["id", "Name"]
          },
          {
            "path": "/api/v1/sound_requirements/",
            "methods": ["GET"],
            "description": "Lista requisitos de som",
            "authentication_required": true,
            "response_model": "sound",
            "fields": ["id", "Name"]
          },
          {
            "path": "/api/v1/image_requirements/",
            "methods": ["GET"],
            "description": "Lista requisitos de imagem",
            "authentication_required": true,
            "response_model": "image",
            "fields": ["id", "Name"]
          },
          {
            "path": "/api/v1/local_wifi/",
            "methods": ["GET"],
            "description": "Lista configurações de Wi-Fi local",
            "authentication_required": true,
            "response_model": "localwifi",
            "fields": ["id", "Name"]
          },
          {
            "path": "/api/v1/events/",
            "methods": ["GET"],
            "description": "Logs de eventos da API (apenas do próprio usuário)",
            "authentication_required": true,
            "response_model": "APILogsModel",
            "fields": ["id", "user", "added_on", "method", "api", "client_ip_address", "status_code", "execution_time", "response"],
            "filters": ["?Start={date}", "?End={date}"]
          },
          {
            "path": "/api/v1/rides/",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "description": "API de passeios (incluída do app rides)",
            "authentication_required": true
          }
        ]
      },
      "partner": {
        "description": "API para gerenciamento de parceiros",
        "base_path": "/partner/",
        "endpoints": [
          {
            "path": "/partner/signup/",
            "methods": ["POST"],
            "description": "Registro de novo parceiro",
            "authentication_required": false,
            "form_fields": ["username", "password1", "password2", "email"]
          },
          {
            "path": "/partner/login/",
            "methods": ["POST"],
            "description": "Login de parceiro",
            "authentication_required": false,
            "form_fields": ["username", "password"]
          },
          {
            "path": "/partner/logout/",
            "methods": ["GET"],
            "description": "Logout",
            "authentication_required": true
          },
          {
            "path": "/partner/password/",
            "methods": ["POST"],
            "description": "Alteração de senha",
            "authentication_required": true
          },
          {
            "path": "/partner/clientProfile/{id}/",
            "methods": ["GET", "PUT"],
            "description": "Atualização de perfil do parceiro",
            "authentication_required": true
          },
          {
            "path": "/partner/contactAdd/",
            "methods": ["POST"],
            "description": "Adicionar contato (POC)",
            "authentication_required": true
          },
          {
            "path": "/partner/contactUpdate/{id}/",
            "methods": ["GET", "PUT"],
            "description": "Atualizar contato",
            "authentication_required": true
          },
          {
            "path": "/partner/contactDelete/{id}/",
            "methods": ["DELETE"],
            "description": "Remover contato",
            "authentication_required": true
          },
          {
            "path": "/partner/localAdd/",
            "methods": ["POST"],
            "description": "Adicionar área de cobertura",
            "authentication_required": true
          },
          {
            "path": "/partner/localUpdate/{id}/",
            "methods": ["GET", "PUT"],
            "description": "Atualizar área de cobertura",
            "authentication_required": true
          },
          {
            "path": "/partner/localDelete/{id}/",
            "methods": ["DELETE"],
            "description": "Remover área de cobertura",
            "authentication_required": true
          },
          {
            "path": "/partner/searchTransactions/{start}/{end}/",
            "methods": ["GET"],
            "description": "Buscar transações por período",
            "authentication_required": true,
            "parameters": {
              "start": "Data início (YYYY-MM-DD)",
              "end": "Data fim (YYYY-MM-DD)"
            }
          },
          {
            "path": "/partner/searchRequests/{start}/{end}/",
            "methods": ["GET"],
            "description": "Buscar requisições API por período",
            "authentication_required": true
          },
          {
            "path": "/partner/searchLogin/{start}/{end}/",
            "methods": ["GET"],
            "description": "Buscar logs de login por período",
            "authentication_required": true
          }
        ]
      },
      "documentation": {
        "description": "Documentação e esquema da API",
        "endpoints": [
          {
            "path": "/docs/",
            "methods": ["GET"],
            "description": "Documentação interativa da API",
            "authentication_required": false
          },
          {
            "path": "/openapi",
            "methods": ["GET"],
            "description": "Esquema OpenAPI",
            "authentication_required": false
          }
        ]
      }
    },
    "data_models": {
      "core_models": [
        "time_zone", "Language", "Currency", "country", "districtregion", 
        "citymunicipality", "usertype", "userprofile", "userloginlog", 
        "events", "RideDuration", "equipment", "publicevent", "sound", 
        "image", "localwifi", "version"
      ],
      "supplier_models": [
        "requisitiontype", "selectiontype", "offertype", "informationtype",
        "identificationtype", "protocol", "profileagency", "reprecategory",
        "profilerepresentative", "contracttype", "contractpaymenttype",
        "contractpricetype", "contract", "contractsection", 
        "contractsectionchannels", "servicetype", "commtype", "NUTSRegion"
      ],
      "partner_models": [
        "profilepartner", "jobpoc", "partnerpoc", "coverage"
      ]
    },
    "authentication_flows": {
      "partner_registration": {
        "steps": [
          "POST /partner/signup/",
          "Login automático após registro",
          "Configurar perfil em /partner/clientProfile/{id}/",
          "Adicionar áreas de cobertura em /partner/localAdd/",
          "Adicionar contatos em /partner/contactAdd/",
          "Ativar API no perfil para obter token"
        ]
      },
      "api_integration": {
        "steps": [
          "Obter token via admin Django ou perfil parceiro ativado",
          "Usar header: Authorization: Token {token}",
          "Acessar endpoints /api/v1/*"
        ]
      }
    },
    "api_logging": {
      "enabled": true,
      "database_logging": true,
      "skip_urls": ["events"],
      "excluded_keys": ["password", "token", "access", "refresh"],
      "methods_logged": ["GET", "POST", "DELETE", "PUT"],
      "status_codes_logged": ["200", "400", "404", "500"]
    },
    "settings": {
      "datetime_format": "YYYY-MM-DDTHH:mm:ss.SSSZ",
      "timezone": "UTC",
      "default_language": "en-us",
      "supported_languages": ["en", "pt"],
      "debug_mode": false,
      "allowed_hosts": ["127.0.0.1", "api.greenconnections.eu", "localhost"],
      "csrf_trusted_origins": ["https://api.greenconnections.eu"]
    }
  }
}
```

## Principais Características da API:

1. **Autenticação Dupla**:
   - Token Authentication para APIs REST (/api/v1/*)
   - Session Authentication para interface web (/partner/*)

2. **Arquitetura Modular**:
   - Core: Dados de referência e configuração
   - Partner: Gerenciamento de parceiros
   - Supplier: Fornecedores e contratos
   - Rides: Funcionalidades de passeios (referenciado mas não incluído no arquivo)

3. **Recursos Principais**:
   - Gestão de parceiros e seus perfis
   - Catálogo de referência (países, moedas, idiomas, etc.)
   - Sistema de contratos com fornecedores
   - Mapeamento NUTS para códigos postais europeus
   - Logs detalhados de API

4. **Segurança**:
   - CSRF protection habilitada
   - Tokens de API
   - Logs de autenticação
   - Filtro de dados sensíveis nos logs

5. **Documentação**:
   - OpenAPI schema disponível em /openapi
   - Documentação interativa em /docs/

A API segue padrões RESTful para endpoints de dados (/api/v1/*) e usa padrões web tradicionais para a interface de parceiros (/partner/*).