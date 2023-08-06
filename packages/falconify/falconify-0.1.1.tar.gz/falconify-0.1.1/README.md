The Scaffolding tool for Falconify.

This scaffolding tool includes a set of commands that allows you to bootstrap your modules following the suggested structure for the Falconify template.

Scaffold usage:  
Start a project: `falconify bootstrap`  
Boot a module: `falconify create-module Pricing or Pricing_Tier`

This will create:    

**Bridging:**    
* The Command Handler: - this will create a new directory under Application/Features and it will place the handler there. You don't need to modify anything here.  
  
**Port:**  
* The Request Handler: - this will create a new directory under Application/Infrastructure/Port/Request and it will place the handler there. You don't need to modify anything here.  
* The Router: - this will create a new file and add it to the Application/Infrastructure/Port/Request/. You don't need to modify anything here for your general CRUD.  
* The Transformer: - this will create a new transformer under Application/Infrastructure/Port/Transformer. You will need to modify this file to implement your contract.  
  
**Adapter**:  
* The Repository: - this will create a new file on Adapters/Repository. You will need to modify the methods (create / update) in this file to fulfil your data requirements  
  
**Domain:**  
* The Model: - this will create a new file on Domain/Model. You will need to model your object in this file.  
* The Use Case: - this will create a new file on Domain/UseCases. You don't need to do much in this file, unless you're doing something out of the normal CRUD. But yes, your business logic should be implemented here.  
Once all of this is done, you can implement your route on Application/Main.py, by:  
  
Importing your new route - found on Application/Infrastructure/Port/Request/Routes.py  
To invoke the route by: Routes().define(self)  
  
**You're ready to consume.**    
This does not cater for migration. Falconify currently uses alembic to manage the migrations.  
