# Asset Conversion Service [omni.services.assets.convert]

## About

A simple extension demonstrating writing a microservice to convert assets using Omniverse Kit-based applications.

## Usage

Once enabled, the extension will expose a `/assets/convert` service endpoint, which can be explored from the list of available microservice endpoints exposed by the application:

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
    --ext-folder C:\Users\<username>\AppData\Local\ov\pkg\farm-queue-102.1.0\exts-farm-queue ^
    --ext-folder ./exts ^
    --enable omni.services.assets.convert
```

**On Linux:**
```shell
# Link the extension against a Kit-based application from the Launcher:
./link_app.sh ~/.local/share/ov/pkg/create-2021.3.7

# Launch Create, with the extension enabled:
./app/omni.create.sh \
    --ext-folder ~/.local/share/ov/pkg/farm-queue-102.1.0/exts-farm-queue \
    --ext-folder ./exts \
    --enable omni.services.assets.convert
```

To launch this small demo pipeline, all that remains is integrating some UI components to let Users submit tasks to the service, or start one from the command-line:
```shell
curl -X 'POST' \
  'http://localhost:8011/assets/convert' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "import_path": "/full/path/to/source_content.usd",
  "output_path": "/full/path/to/destination_content.obj",
  "converter_settings": {}
}'
```
