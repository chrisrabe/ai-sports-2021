Explore some other time. Use forwarder bot to run simulations. Stretch.

Include this in base-compose.yml when ready
```
    python3-fwd:
        build:
            context: python3
            dockerfile: Dockerfile.fwd

    python3-fwd-dev:
        build:
            context: python3
            dockerfile: Dockerfile.fwd.dev
        volumes:
            - ./python3:/app
```
