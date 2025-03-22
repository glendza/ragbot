.PHONY:  clean-pyc install_cli_completions generate_cli_docs sync

clean-pyc:
	@find . -name \*.pyc -delete

install_cli_completions:
	@ragbot-cli --install-completion

generate_cli_docs:
	@mkdir -p docs
	@typer ragbot.cli utils docs --name "ragbot" --output docs/ragbot_cli.md --title "Ragbot CLI"

sync:
	@uv sync \
		--extra dev \
		--extra discord \
		--extra openai \
		--extra mistralai \
		--extra jina \
		--extra domains
