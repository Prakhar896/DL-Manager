# DL-Manager

This is a DeepLens Manager that allows you to easily interact with your DeepLens without having to SSH everytime. See the [Usage Documentation](/usage.md) to learn more.

## Activator

<img src="https://github.com/Prakhar896/ActivatorDocs/blob/main/activatorLogo.png?raw=true" alt="Activator Logo" width="350px">

[Activator](https://github.com/Prakhar896/ActivatorDocs) is a product activation service that activates copies. It also provides users a unified dashboard to manage all of your activated copies across several products that conform to Activator's DRM (Digital Rights Management) process. DeepLens Manager (or DLM) is one of these products.

### How It Works

Any copy of DLM will first need to be activated with Activator. You do not have to do anything on your part; upon boot, if not activated, DLM will locate the latest Activator server and will activate itself. A `licensekey.txt` file will be downloaded that will contain the license key for the copy. This file will be used to verify the copy's authenticity.

**DO NOT** delete the `licensekey.txt` file. If you do, the copy will be deactivated and will need to be activated again.

Every 14 days, the copy will automatically trigger a license key verification request (KVR) to ensure that the copy is still activated. If the copy is not activated, it will be deactivated and will need to be activated again. (Run the copy code again.)

### What I Can Do With Activator

During copy activation, the activation script generates unique identifiers for the computer it is being run on (called HSN) and for the copy itself (called CSN).

These identifiers are submitted to Activator servers. If an account with the same HSN is found, the CSN is added to the account. If no account is found, a new account is created with the HSN and CSN.

> NOTE: None of your private computer information is divulged in the activation process.

Then, you can log in to Activator using the link provided in the `licensekey.txt` file. You will be able to see all of your activated copies and their CSNs. You can also manage your account, link other HSN accounts as aliases and much more.

> For more information about Activator, see its [documentation](https://github.com/Prakhar896/ActivatorDocs)


© 2022 Prakhar Trivedi