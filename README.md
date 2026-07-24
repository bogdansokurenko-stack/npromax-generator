# npromax-generator

Генератор статического сайта **www.npromax.com.ua** (собственная ТМ кофе NPROMAX).

## Состав
- `build_site.py` — генератор HTML (Python, без внешних зависимостей). Читает данные о товарах и пишет ~159 HTML + assets.
- `build_lib.py` — вспомогательные функции для `build_site.py`.

## Как это деплоится
Сервер (adm.tools, `/home/npro/npromax-sync/`) по ночному cron делает `git pull` этого репозитория,
копирует `build_site.py` + `build_lib.py` поверх рабочих копий и запускает пайплайн синхронизации с Prom.
Чтобы обновить прод: изменить генератор → `git push` → запустить sync.

## Чего здесь НЕТ (умышленно, остаётся только на сервере)
- `sync.sh` — содержит секретный токен Prom-фида (`hash_tag`). **Никогда не коммитить.**
- `parse_feed.py` — парсер Prom-фида (стабильный, живёт на сервере).
- `site_products.json`, `prom_feed.xml` — данные, генерируются на сервере.

## Запуск (локально)
```bash
NPROMAX_SITE=./out NPROMAX_SRC=./site_products.json python3 build_site.py
```
