from crewai import Task


def create_send_tour_request_task(agent):
    return Task(
        description="""
        Send an apartment tour request email using the MCP tool `send_apartment_tour_request`.

        Inputs:
        - landlord_email: {landlord_email}
        - tenant_name: {tenant_name}
        - property_address: {property_address}
        - preferred_date: {preferred_date}
        - preferred_time: {preferred_time}
        - tenant_phone: {tenant_phone}
        - message: {message}

        Rules:
        1) If required fields are missing, return a clear message listing missing fields.
        2) If required fields are present, call `send_apartment_tour_request`.
        3) Return the tool result exactly, plus one friendly confirmation sentence.
        """,
        expected_output="""
        A concise result indicating whether the tour request email was sent successfully.
        Includes any failure reason from the tool if sending failed.
        """,
        agent=agent,
    )