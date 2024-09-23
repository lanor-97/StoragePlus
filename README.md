# StoragePlus & UniversalBox

University project demonstrating remote file management using both a Command Line Interface (CLI) application and a web application, **UniversalBox**.

## Introduction

**StoragePlus** is a service that enables remote file management. It allows users to upload, download, and delete files stored on a server, provided they have registered for the service. StoragePlus is designed to be used via a CLI application that takes user commands and converts them into appropriate HTTPS requests sent to the server.

**UniversalBox** is a web application that provides a user-friendly interface for StoragePlus, allowing users to manage their files through a web-based platform.

## Features

The project consists of two main components:

1. **CLI Application**: 
   - Allows interaction with StoragePlus to perform basic functions: login, registration, retrieving a list of files on the server, downloading, uploading, or deleting files.
  
2. **UniversalBox Web Application**:
   - Provides a simpler way to perform file operations through a web interface.
   - Users must already have a StoragePlus account to use UniversalBox.
   - Registered UniversalBox users can perform file operations directly through the web interface, based on their subscription plan:
     - **Basic Plan**: Can only download files.
     - **Premium Plan**: Can download and upload files.
     - **Deluxe Plan**: Can download, upload, and delete files.

## Technical Details

- Both **StoragePlus** and **UniversalBox** are implemented using **Flask** (Python).
- The CLI application is an interactive Python script that utilizes the `requests` library to communicate with the server.
- Both StoragePlus and UniversalBox have their own local **SQLite** databases, managed using **SQLAlchemy**. These databases store user data and other OAuth2 entities (tokens, clients, authorization codes).
- **StoragePlus** exposes APIs for both the CLI application and UniversalBox to use (OAuth2 APIs are used exclusively by UniversalBox).
- OAuth2 functionalities are implemented using the **Authlib** library, supporting the **Authorization Code** flow, allowing UniversalBox to securely access StoragePlus on behalf of the user.

### OAuth2 Integration

- The OAuth2 flow grants access to three different scopes based on the user plan: `download`, `upload`, and `delete`.
- Verification of the OAuth2 scopes is performed on the client-side. UniversalBox uses the appropriate OAuth2 client based on the user’s subscription plan.
- The OAuth2 `Authorization Code` flow results in an access token stored in UniversalBox's local database, linked to the requesting user.

## Security

- The web servers use **self-signed certificates** as they are hosted locally. The cipher suite used is **TLS_AES_256_GCM_SHA384**, which utilizes **SHA-384** to compute an HMAC for data integrity checks.
- The servers use **TLS 1.3**, providing:
  - **Authentication**: The server is always authenticated, while client authentication is optional.
  - **Data Integrity**: Ensures data sent and received can't be tampered with without detection.
  - **Confidentiality**: Data is readable only by the sender and the receiver.

- For OAuth2 token endpoint authentication, UniversalBox uses the `client_secret_post` method as per **RFC7591**, where the client sends data using HTTP POST parameters.
- Upon successful authorization, the access token is stored in the local database of UniversalBox, associated with the corresponding user.
- The `state` parameter for OAuth2 requests is managed automatically by the **Authlib** library, ensuring protection against **Cross-Site Request Forgery (CSRF)** attacks.
