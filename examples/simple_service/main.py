from scottzach1.pif import providers, wiring


class ApiClient:
    """
    An API client that takes a domain and token.
    """

    def __init__(self, domain: str, token: str):
        assert domain and token

    def do_stuff(self): ...


# Define some providers to use for injection.
ApiDomainProvider = providers.Blank()
ApiTokenProvider = providers.Blank()
ApiClientProvider = providers.Singleton(ApiClient, domain=ApiDomainProvider, token=ApiTokenProvider)


@wiring.inject
def main(client: ApiClient = ApiClientProvider):
    """
    Your application logic.
    """
    client.do_stuff()


if __name__ == "__main__":
    ApiDomainProvider.override_existing("example.domain.com")
    ApiTokenProvider.override_existing("*****")

    main()
