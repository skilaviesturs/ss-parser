SHELL := /bin/bash
.PHONY: ps update start stop deploy

help:
	@echo ""
	@echo "🛠️  Pieejamās Make komandas:"
	@echo ""
	@echo "  make ps        # Display running Docker containers"
	@echo "  make clean		  # Tīra docker konteinerus un attēlus"
	@echo "  make update 		# Force-pull izmaiņas no git"
	@echo "  make start     # Build and start Docker containers"
	@echo "  make stop			# Stop and remove Docker containers"
	@echo "  make deploy		# Pilns deploy: stop → update → start"
	@echo ""

ps:
	@echo "📦 Docker konteineru saraksts"
	@sudo docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}" -a

clean:
	@echo "🧹 Tīra docker konteinerus un attēlus"
	@sudo docker system prune -f --volumes

# Force-pull izmaiņas no git
update:
	@bash ./scripts/git-pull-from-repo.bash
	@echo "✅ Git repository force updated from origin/main"

# Build + start Docker konteinerus
start:
	@sudo docker compose up --build -d
	@echo "🚀 Docker containers built and started"

# Stop + remove Docker konteinerus
stop:
	@sudo docker compose down
	@echo "🛑 Docker containers stopped and removed"

# Pilns deploy: stop → update → start
deploy: stop clean update start ps
	@echo "🎉 Deployment completed"
