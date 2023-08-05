# zabel-fabric

The high-level **zabel.fabric** library.

**Please note that this library is in alpha.  It's not stable yet.**

It provides an abstraction for _realms_, which are collections of
platforms and domains taht handles users and managed projects.

It also provides an abstraction for _platforms_, which are collections of
_services_.

## Services (Abstract Base Classes)

### Realm Abstract Class

**work in progress, not ready yet**

| Abstract&nbsp;Class | Description                                    |
| ------------------- | ---------------------------------------------- |
| _Realm_             | A collection of platforms and domains.  A realm handles users and managed projects, and implements the _Service_ interface.           |

### Platform Abstract Class

| Abstract&nbsp;Class | Description                                    |
| ------------------- | ---------------------------------------------- |
| _Platform_         | A service that manages a collection of managedservices and utilities services, with an associated set of properties and datasources. A platform handles users and managed projects, and implements _Service_ interface.       |

## Properties Helper Classes

### Managed accounts

| Helper&nbsp;Class        | Description                               |
| ------------------------ | ----------------------------------------- |
| _ManagedAccount_        | An abstract class that represents a minimal managed account.                  |
| _ManagedAccountManager_ | An abstract class that handles collections of managed accounts.                      |

### Managed projects

| Helper&nbsp;Class                        | Description               |
| ---------------------------------------- | ------------------------- |
| _DomainProviderManagedProjectDefinition_ | An abstract class that extends the _ManagedProjectDefinition_ class to cover common managed project definition needs.                    |
| _ManagedProjectDefinitionManager_       | An abstract class that handles collections of managed project definitions.              |

## Datasources Helper Classes

| Helper&nbsp;Class   | Description                                    |
| ------------------- | ---------------------------------------------- |
| _Storage_           | An interface for storage classes.              |
| _ObjectStorage_     | An interface for storage classes handling one object.                                        |
| _CollectionStorage_ | An interface for storage classes handling a collection of objects.                         |
| _AWSS3Storage_      | An abstract class providing AWS S3 helpers.    |
| _AWSS3Object_       | A _Storage_ class for JSON files stored on a S3 bucket.                                     |
| _AWSS3Bucket_       | A _Storage_ class for handling S3 buckets.     |
| _ManagedDict_       | A simple class making use of an _ObjectStorage_ delegate, providing a 'persistent' dictionary. |
