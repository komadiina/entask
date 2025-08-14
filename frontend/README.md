# entask-frontend

### docker installation

run `docker compose up` (with `-d` for detached mode) to run the composition.

### upon modifying:

run `docker compose up --force-recreate` to recreate the containers.
if the `package.json` is edited, run `docker compose exec frontend npm install` to modify/install/remove the linux binaries inside the container (or via `exec` terminal in docker desktop) -- node_modules is **not** bind-mounted

### TODOs

- implement HttpOnly cookie-based authentication
