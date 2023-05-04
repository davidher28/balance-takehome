import graphene
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from app.graphql.resolvers import Query
from app.utils.merge import MergeSyncUtil

app = FastAPI(
    title="Balance Takehome",
    desciption="Balance Takehome - Integration with merge.dev Unified API",
)

origins = ["http://localhost:8000", "https://localhost:5050", "http://localhost"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_route = {
    "schema": graphene.Schema(query=Query),
    "on_get": make_graphiql_handler(),
}
app.mount("/graphql", GraphQLApp(**graphql_route))

asycn_scheduler = AsyncIOScheduler()
asycn_scheduler.start()


@app.on_event("startup")
async def ingestion_process():
    """Ingestion process in charge of polling and upserting data."""

    sync_util = MergeSyncUtil()
    sync_util.sync_companies()
    sync_util.sync_accounts()
    sync_util.sync_transactions()
    sync_util.sync_status_repository.add()


"""
    Coroutine scheduled with a 24 hours interval due to the Frequency instructions defined by merge.dev.
    See https://docs.merge.dev/integrations/accounting/quickbooks-online/sync-frequencies
"""
asycn_scheduler.add_job(ingestion_process, "interval", seconds=6 * 60 * 60)
