from datetime import datetime, timedelta


async def ensure_valid_token(hass, entry):
    data = hass.data["revoltab"][entry.entry_id]

    if datetime.utcnow() < data["expires_at"] - timedelta(minutes=2):
        return data["tokens"]["access_token"]

    oauth = data["oauth"]
    tokens = data["tokens"]

    new_tokens = await oauth.refresh(tokens["refresh_token"])

    expires_at = datetime.utcnow() + timedelta(
        seconds=new_tokens["expires_in"]
    )

    data["tokens"] = new_tokens
    data["expires_at"] = expires_at

    hass.config_entries.async_update_entry(
        entry,
        data=new_tokens,
    )

    return new_tokens["access_token"]
