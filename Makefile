.PHONY: update start stop deploy

# Force-pull izmaiņas no git
update:
	@bash ./scripts/git-pull-from-repo.bash
	@echo "✅ Git repository force updated from origin/main"

# Build + start Docker konteinerus
start:
	@docker compose up --build -d
	@echo "🚀 Docker containers built and started"

# Stop + remove Docker konteinerus
stop:
	@docker compose down
	@echo "🛑 Docker containers stopped and removed"

# Pilns deploy: stop → update → start
deploy: stop update start
	@echo "🎉 Deployment completed"
