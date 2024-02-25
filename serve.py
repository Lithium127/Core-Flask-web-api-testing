from app import create_app, config

selected_config = config.DevelopmentConfig()
create_app(selected_config).run(
    host = "127.0.0.1",
    port = 5000
)