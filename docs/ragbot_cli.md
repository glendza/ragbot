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
* `tinydb`: Manage TinyDB database and its tables.

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
* `search`: Semantic search in the Milvus vector...

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

### `ragbot milvus search`

Semantic search in the Milvus vector database.

**Usage**:

```console
$ ragbot milvus search [OPTIONS] QUERY
```

**Arguments**:

* `QUERY`: [required]

**Options**:

* `--help`: Show this message and exit.

## `ragbot tinydb`

Manage TinyDB database and its tables.

**Usage**:

```console
$ ragbot tinydb [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `truncate-table`: Truncate a table in the TinyDB database.

### `ragbot tinydb truncate-table`

Truncate a table in the TinyDB database.

**Usage**:

```console
$ ragbot tinydb truncate-table [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
