## More Docs

### char_lib_30
The char_lib_30 model ('export.pkl) will need to be obtained securely, along with the 'map.json' file, from the R2 Data
Labs team as this contains confidential RR IP. 
These files should then be placed in the default directory '~HOME/.r2dl_ocr/'. The path to a custom 
directory can be exported as an environment variable instead, as shown below.

```shell
$ export MODEL_INPUT_PATH=/usr/example/char_lib_30/
```

Alternatively, the path to this directory can be provided as an argument to the 'read_cnn_settings' method inside 
the settings class. See documentation for the Settings class for details.
