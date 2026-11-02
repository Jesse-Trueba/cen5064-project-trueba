# Creational Pattern Map

## Factory Method

No genuine fit because the application does not currently have subclasses that need to choose between different variants of one product.

## Abstract Factory

No genuine fit because the application does not create families of related objects that must stay matched together.

## Builder

No genuine fit right now because the main domain objects, such as Budget and Transaction, have straightforward construction and do not have many optional fields or construction stages.

## Prototype

No genuine fit because the application does not currently create new budgets or transactions by cloning configured templates.

## Singleton

Genuine fit for application configuration. The application has one shared default database configuration that should remain consistent across repositories. A single AppConfig instance can hold that configuration and be injected into the repositories that need it.

## Best Fit

Singleton is the best fit because the application needs one shared configuration for resources such as the database path. Using one AppConfig instance keeps this configuration consistent while still allowing the configuration to be injected into other classes rather than accessed as hidden global state.