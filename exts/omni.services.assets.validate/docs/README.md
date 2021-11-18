# Asset Validation Service [omni.services.assets.validate]

## About

A simple extension demonstrating writing a microservice to validate assets using Omniverse Kit-based applications.

## Usage

Once enabled, the extension will expose a `/assets/validate` service endpoint, which can be explored from the list of available microservice endpoints exposed by the application:

 * For *Kit*: http://localhost:8011/docs
 * For *Create*: http://localhost:8111/docs
 * For *Isaac Sim*: http://localhost:8211/docs

## Running the extension

To enable and execute the extension, from the root of the repository:

**On Windows:**
```batch
REM Link the extension against a Kit-based application from the Launcher:
link_app.bat C:/Users/<username>/AppData/Local/ov/pkg/create-2021.3.7

REM Launch Create, with the extension enabled:
app/omni.create.bat ^
    --ext-folder ./exts ^
    --enable omni.services.assets.validate
```

**On Linux:**
```shell
# Link the extension against a Kit-based application from the Launcher:
./link_app.sh ~/.local/share/ov/pkg/create-2021.3.7

# Launch Create, with the extension enabled:
./app/omni.create.sh \
    --ext-folder ./exts \
    --enable omni.services.assets.validate
```
