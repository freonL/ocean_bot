from ibm_watson import AssistantV1,AssistantV2, PersonalityInsightsV3
from pymessenger.bot import Bot

# Database SQL Lite
DB_NAME = "example.db"

# FB Messenger setting
fb_bot = Bot("EAAT4M6dGO0QBAN3WafZBlK4240GGwNgFZA4aBZC9K9tKqvkbPq1UEHoEpvg5dWZCM0SXIJaZAzX94j24joTAR3OTUzDwxoMneAKxl3EaZBzVrVzkj6TFgiFTDwth09EDE6uUw2yxqZCkBI8IHsidTIvW3K3pcJUgPEk551XmqmZBXgZDZD")
VERIFY_TOKEN = "5071ccd7-c9a6-414c-852a-3c3b03453c24"

anna_bot = Bot("EAAhmgsKcEfsBAMTMXZC78zdGy4OpXaodixPQ6tjIFi4tiXQaA2K1oPz6XUVEOi9VnuLNXdVqItuuZAj45TUpgVmyBUtYOJajhUqhsMDKvFTzZAiVmH4eFBvR35g3AKoLSrYFhDUjVekwiCMe4dYJAR1PoJk2ZCldL0xg7zyr7gZDZD")
anna_token = ""

belle_Bot = Bot("EAAJnGyIJHkEBANn1Wz7WDWSf4FrmZBjCgWmWNBXT3LcobXVsH3GlDeUIuzWHHM0JT8DbQTahi7H1Eom4vNDFYKnoLovgnzQEYEPPLZATncyoK7ObIu6Xcmyj60fR14t1Xs2u2jOjKwwjB1OOlUOUgSpOuRQ0d32ppOCCRI1wZDZD")
belle_token = ""

# IBM Watson 
personality_insights = PersonalityInsightsV3(
    version    = "2017-10-13",
    iam_apikey = "gYf7-1OzOB8-hzPK6Wunde9aAV9DW5VYA93RaIGvNE1m",
    url        = "https://gateway-syd.watsonplatform.net/personality-insights/api"
)

assistant = AssistantV2(
    version    = "2019-02-28",
    iam_apikey = "0B2HITIOQodvrG9zEnBsFBZQHteLtpYBEqS2KECTCMkV",
    url        = "https://gateway-syd.watsonplatform.net/assistant/api"
)
WORKSPACE_ID  = "3819733a-016d-4f53-bdc2-61a151e55822"

ASSISTANT_ID  = "fa7f1040-f02d-4caf-9e24-0eb86ca659df"
ASSISTANT_URL = "https://gateway-syd.watsonplatform.net/assistant/api/v2/assistants/fa7f1040-f02d-4caf-9e24-0eb86ca659df/sessions"
