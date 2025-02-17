# Ragbot CLI

Ragbot tools.

**Usage**:

```console
$ ragbot [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `milvus`: Manage Milvus DB and its collections.

## `ragbot milvus`

Manage Milvus DB and its collections.

**Usage**:

```console
$ ragbot milvus [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `init`: Initialize the Milvus vector database with...
* `drop-collection`: Drop a collection from the Milvus vector...
* `import-data`: Import data into the Milvus vector database.

### `ragbot milvus init`

Initialize the Milvus vector database with the required collections.

**Usage**:

```console
$ ragbot milvus init [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `ragbot milvus drop-collection`

Drop a collection from the Milvus vector database.

**Usage**:

```console
$ ragbot milvus drop-collection [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `ragbot milvus import-data`

Import data into the Milvus vector database.

**Usage**:

```console
$ ragbot milvus import-data [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
