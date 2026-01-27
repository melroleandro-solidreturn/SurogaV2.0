# Ontologia do Projeto SurogaAPI

## 1. Visão Geral
A ontologia representa a estrutura e domínio do **SurogaAPI**, um sistema Django para gestão de serviços de surrogacia de passeios ("rides"). A ontologia abrange três dimensões principais:
- **Estrutura Técnica** do projeto Django (apps, modelos, views, URLs)
- **Domínio de Negócio** (parceiros, fornecedores, passeios, localizações)
- **Mecanismos de Suporte** (autenticação, logging, comunicação assíncrona)

## 2. Classes Principais

### 2.1. Estrutura Técnica
| Classe | Descrição | Exemplos |
|--------|-----------|----------|
| `Project` | Projeto Django completo | SurogaAPI |
| `App` | Aplicação Django | core, supplier, partner, rides |
| `Model` | Modelo de dados (ORM) | time_zone, profilepartner, contract |
| `View` | Lógica de apresentação/API | time_zoneViewSet, ClientDashboard |
| `URL` | Roteamento de endpoints | `/api/v1/time_zones/`, `/partner/login/` |
| `Serializer` | Transformação de dados | time_zoneSerializer, CountrySerializer |
| `Middleware` | Processamento de requisições | APILoggerMiddleware, SecurityMiddleware |
| `Setting` | Configuração do sistema | DEBUG, DATABASES, INSTALLED_APPS |

### 2.2. Domínio de Negócio
| Classe | Descrição | Exemplos |
|--------|-----------|----------|
| `User` | Utilizador do sistema | Admin, Parceiro, Fornecedor |
| `Partner` | Entidade parceira (cliente da API) | App de mobilidade, Empresa de turismo |
| `Supplier` | Fornecedor de serviços | Agência de surrogacia |
| `Ride` | Passeio/viagem surrogate | Passeio de 30min em Lisboa |
| `Booking` | Reserva de passeio | Reserva #1234 |
| `ServiceType` | Tipo de serviço oferecido | Turístico, Corporativo, Evento |
| `Contract` | Contrato com fornecedor | Contrato tipo A, Contrato exclusivo |
| `Location` | Localização geográfica | País, Distrito, Município |

### 2.3. Componentes de Suporte
| Classe | Descrição | Exemplos |
|--------|-----------|----------|
| `AuthenticationToken` | Token de autenticação API | Token 123abc |
| `Log` | Registro de atividade | APILogsModel, userloginlog |
| `EmailThread` | Processo assíncrono de email | EmailThread |
| `CommunicationChannel` | Canal de comunicação | Email CRM, API support |
| `Equipment` | Equipamento necessário | Câmera, Sistema de som |
| `Configuration` | Configuração específica | Versão de endpoint, Timezone |

## 3. Relacionamentos Principais

### 3.1. Relacionamentos Estruturais
```
Project --has--> App
App --contains--> Model
App --contains--> View
App --contains--> URL
Model --has--> Field
Model --representedBy--> Serializer
View --handles--> URL
View --uses--> Serializer
Middleware --processes--> Request/Response
```

### 3.2. Relacionamentos de Domínio
```
User --hasProfile--> (PartnerProfile|SupplierProfile|UserProfile)
Partner --offers--> ServiceType
Supplier --has--> Contract
Contract --covers--> Location
Contract --defines--> ServiceType
Ride --belongsTo--> ServiceType
Ride --has--> Booking
Booking --generates--> Payment
Location --contains--> (Country > DistrictRegion > CityMunicipality)
```

### 3.3. Relacionamentos de Suporte
```
User --authenticatesWith--> AuthenticationToken
APIRequest --loggedAs--> APILog
System --sendsAsync--> EmailThread
Supplier --communicatesThrough--> CommunicationChannel
ServiceType --requires--> Equipment
```

## 4. Propriedades e Atributos

### 4.1. Propriedades de Modelos Principais

**UserProfile:**
- `is_active` (boolean)
- `email_confirmed` (boolean)
- `preferred_language` (Language)
- `user_type` (enum)

**PartnerProfile:**
- `API_activated` (boolean)
- `API_test_mode` (boolean)
- `stripe_id` (string)
- `validated_profile` (boolean)
- `coverage_areas` (list[Location])

**SupplierProfile:**
- `agency_name` (string)
- `contract_type` (enum)
- `service_regions` (list[Location])
- `is_active` (boolean)

**Contract:**
- `contract_type` (A-F)
- `payment_type` (enum)
- `price_type` (enum)
- `start_date` (date)
- `expiration_date` (date)

## 5. Restrições e Regras

### 5.1. Regras de Negócio
1. Um Partner deve ter perfil validado para usar a API em produção
2. Cada ServiceType requer tipos específicos de contrato (A-F)
3. Suppliers só podem oferecer serviços em regiões cobertas por contrato
4. Bookings só podem ser criadas para ServiceTypes ativos

### 5.2. Regras Técnicas
1. Views de API requerem TokenAuthentication
2. Endpoints de leitura são acessíveis a usuários autenticados
3. Endpoints de escrita requerem permissões específicas
4. Logs de API excluem campos sensíveis (password, token)

## 6. Hierarquia de Classes

```
Entity
├── TechnicalEntity
│   ├── Project
│   ├── App
│   ├── Model
│   ├── View
│   └── URL
├── BusinessEntity
│   ├── User
│   │   ├── Partner
│   │   ├── Supplier
│   │   └── Administrator
│   ├── Service
│   │   ├── Ride
│   │   ├── Booking
│   │   └── ServiceType
│   └── Agreement
│       └── Contract
└── SupportEntity
    ├── AuthenticationToken
    ├── Log
    ├── Configuration
    └── CommunicationChannel
```

## 7. Instâncias de Configuração

### 7.1. Configurações do Sistema
- **Ambiente:** Desenvolvimento/Produção
- **Banco de Dados:** SQLite (dev), Azure SQL (prod)
- **Autenticação:** Token-based (DRF)
- **Idiomas:** Inglês, Português
- **Moeda padrão:** EUR
- **Timezone:** UTC

### 7.2. Endpoints Principais
- **API Core:** `/api/v1/time_zones/`, `/api/v1/countries/`
- **Partner:** `/partner/dashboard/`, `/partner/profile/`
- **Documentação:** `/docs/`, `/openapi/`
- **Admin:** `/admin/`

## 8. Fluxos de Trabalho

### 8.1. Fluxo de Registro de Partner
```
1. SignUp → 2. Email Confirmation → 3. Profile Completion → 
4. API Activation → 5. Coverage Definition → 6. Service Integration
```

### 8.2. Fluxo de Contratação de Supplier
```
1. Supplier Registration → 2. Contract Negotiation → 
3. Service Definition → 4. Region Assignment → 
5. Communication Channels Setup → 6. Activation
```

### 8.3. Fluxo de Passeio
```
1. Ride Request → 2. Supplier Matching → 3. Booking Creation → 
4. Payment Processing → 5. Ride Execution → 6. Completion Logging
```

## 9. Anotações e Observações

### 9.1. Design Patterns Identificados
- **Repository Pattern:** Models + Serializers + Viewsets
- **Strategy Pattern:** Diferentes tipos de contrato (A-F)
- **Observer Pattern:** Logging middleware e signals
- **Factory Pattern:** Criação de perfis de usuário
- **Decorator Pattern:** api_client_required decorator

### 9.2. Considerações de Segurança
- Tokens de API para autenticação
- Exclusão de dados sensíveis em logs
- Validação de perfis antes da ativação
- Middleware de proteção CSRF e clickjacking

### 9.3. Escalabilidade
- Suporte a múltiplos idiomas e moedas
- Design baseado em microserviços (apps independentes)
- Logging assíncrono com batching
- Configuração para deployment em nuvem (Azure)

## 10. Glossário

| Termo | Definição |
|-------|-----------|
| **Surrogate Ride** | Passeio realizado por terceiro em nome do usuário |
| **Partner** | Cliente que integra a API em sua aplicação |
| **Supplier** | Provedor dos serviços de passeio |
| **ServiceType** | Categoria de serviço oferecido |
| **Coverage** | Área geográfica coberta por um serviço |
| **Contract Section** | Cláusula específica de um contrato |
| **API Logger** | Sistema de log de requisições/respostas da API |

---

Esta ontologia fornece uma representação abrangente do ecossistema SurogaAPI, capturando tanto aspectos técnicos quanto de domínio de negócio, facilitando a compreensão, documentação e evolução do sistema.