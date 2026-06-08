import voluptuous as vol

from homeassistant import config_entries

from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_URL,
    CONF_IGNORED_GROUPS
)


class BakalariConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_NAME): str,
            vol.Required(CONF_URL): str,
            vol.Optional(
                CONF_IGNORED_GROUPS,
                default=""
            ): str
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )