import typer
from pymilvus import CollectionSchema, DataType, FieldSchema, MilvusClient
from rich.console import Console

from ragbot.container import RagbotContainer

console = Console()


cli = typer.Typer(
    name="Milvus",
    help="Manage Milvus DB and its collections.",
    add_completion=True,
)


@cli.command(
    name="init",
    help="Initialize the Milvus vector database with the required collections.",
)
def init_milvus() -> None:
    # Bootstrap the container:
    app_container = RagbotContainer.from_default_config()

    milvus_uri = app_container.config.milvus.uri()
    if not milvus_uri:
        console.print("Milvus URI not set. Skipping initialization.")
        return

    milvus_collection_name = app_container.config.milvus.collection_name()
    if not milvus_collection_name:
        console.print("Milvus collection name not set. Skipping initialization.")
        return

    vector_dimension = app_container.config.milvus.vector_dim()
    if not vector_dimension:
        console.print("Milvus vector dimension not set. Skipping initialization.")
        return

    # Init the sync Milvus client:
    milvus_client = MilvusClient(milvus_uri)

    # Check if the collection already exists:
    if milvus_client.has_collection(collection_name=milvus_collection_name):
        console.print(f"Collection '{milvus_collection_name}' already exists. Skipping initialization.")
        return

    console.print(f"Creating collection '{milvus_collection_name}'")

    schema = CollectionSchema(
        [
            FieldSchema(
                name="id",
                dtype=DataType.INT64,
                is_primary=True,
                auto_id=True,
            ),
            FieldSchema(
                name="content",
                dtype=DataType.VARCHAR,
                max_length=65535,
            ),
            FieldSchema(
                name="vector",
                dtype=DataType.FLOAT_VECTOR,
                dim=vector_dimension,
            ),
        ]
    )

    milvus_client.create_collection(
        collection_name=milvus_collection_name,
        schema=schema,
    )

    index_params = milvus_client.prepare_index_params()
    index_params.add_index(
        field_name="vector",
        metric_type="COSINE",
        index_type="IVF_FLAT",
        index_name="vector_index",
        params={
            "nlist": 128,
        },
    )

    milvus_client.create_index(
        collection_name=milvus_collection_name,
        index_params=index_params,
        sync=False,
    )

    console.print(f"Collection '{milvus_collection_name}' created successfully.")
