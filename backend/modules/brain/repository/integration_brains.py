from models.settings import get_supabase_client
from modules.brain.entity.integration_brain import (
    IntegrationDescriptionEntity,
    IntegrationEntity,
)
from modules.brain.repository.interfaces.integration_brains_interface import (
    IntegrationBrainInterface,
    IntegrationDescriptionInterface,
)


class IntegrationBrain(IntegrationBrainInterface):
    """This is all the methods to interact with the integration brain.

    Args:
        IntegrationBrainInterface (_type_): _description_
    """

    def __init__(self):
        self.db = get_supabase_client()

    def get_integration_brain(self, brain_id, user_id):
        response = (
            self.db.table("integrations_user")
            .select("*")
            .filter("brain_id", "eq", brain_id)
            .filter("user_id", "eq", user_id)
            .execute()
        )
        if len(response.data) == 0:
            return None

        return IntegrationEntity(**response.data[0])

    def add_integration_brain(self, brain_id, user_id, integration_id, settings):

        response = (
            self.db.table("integrations_user")
            .insert(
                [
                    {
                        "brain_id": str(brain_id),
                        "user_id": str(user_id),
                        "integration_id": str(integration_id),
                        "settings": settings,
                    }
                ]
            )
            .execute()
        )
        if len(response.data) == 0:
            return None
        return IntegrationEntity(**response.data[0])

    def update_integration_brain(self, brain_id, user_id, integration_brain):
        response = (
            self.db.table("integrations_user")
            .update(integration_brain.dict(exclude={"brain_id", "user_id"}))
            .filter("brain_id", "eq", str(brain_id))
            .filter("user_id", "eq", str(user_id))
            .execute()
        )
        if len(response.data) == 0:
            return None
        return IntegrationEntity(**response.data[0])

    def delete_integration_brain(self, brain_id, user_id):
        self.db.table("integrations_user").delete().filter(
            "brain_id", "eq", str(brain_id)
        ).filter("user_id", "eq", str(user_id)).execute()
        return None


class IntegrationDescription(IntegrationDescriptionInterface):

    def __init__(self):
        self.db = get_supabase_client()

    def get_integration_description(self, integration_id):
        response = (
            self.db.table("integrations")
            .select("*")
            .filter("id", "eq", integration_id)
            .execute()
        )
        if len(response.data) == 0:
            return None

        return IntegrationDescriptionEntity(**response.data[0])

    def get_integration_description_by_user_brain_id(self, brain_id, user_id):
        response = (
            self.db.table("integrations_user")
            .select("*")
            .filter("brain_id", "eq", brain_id)
            .filter("user_id", "eq", user_id)
            .execute()
        )
        if len(response.data) == 0:
            return None

        integration_id = response.data[0]["integration_id"]
        return self.get_integration_description(integration_id)

    def get_all_integration_descriptions(self):
        response = self.db.table("integrations").select("*").execute()
        return [IntegrationDescriptionEntity(**data) for data in response.data]
