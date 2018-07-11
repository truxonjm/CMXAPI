# CMXAPI

##### Endpoints:

- '/api/v2/client/latest' --- Returns last stored Client
- '/api/v2/client/count' ---- Returns the number of Clients stored in the database
- '/api/v2/client/all' ------ Returns all stored Clients
- '/api/v2/log/latest' ------ Returns last stored RequestLog
- '/api/v2/log/count' ------- Returns the number of RequestLogs stored in the database
- '/api/v2/log/all' --------- Returns all stored RequestLogs
- '/api/v2/cmx/pull' -------- Initiates a 'step' which pulls data from CMX within a certain time period. It then stores this data to the                                   database and creates a RequestLog summarizing the step.

##### Config Structure:

--REQUIRES PROPER DOCUMENTATION--