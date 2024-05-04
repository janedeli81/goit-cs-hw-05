import asyncio
import argparse
from pathlib import Path
import aiofiles
import aiofiles.os
import logging

# Налаштування логера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(source_path: Path, dest_folder: Path):

    if not source_path.is_file():
        return

    # Створення підпапки на основі розширення файлу, якщо така ще не існує
    dest_path = dest_folder / source_path.suffix.removeprefix('.')
    await aiofiles.os.makedirs(dest_path, exist_ok=True)

    # Копіювання файлу
    async with aiofiles.open(source_path, mode='rb') as src, aiofiles.open(dest_path / source_path.name, mode='wb') as dst:
        await dst.write(await src.read())
    logging.info(f'File {source_path} copied to {dest_path / source_path.name}')

async def read_folder(folder: Path, dest_folder: Path):

    async for path in folder.rglob('*'):
        if path.is_file():
            await copy_file(path, dest_folder)

def main():
    parser = argparse.ArgumentParser(description='Sort files from source folder to destination folder based on their extensions.')
    parser.add_argument('--source', required=True, help='Source folder path')
    parser.add_argument('--dest', required=True, help='Destination folder path')

    args = parser.parse_args()

    source_folder = Path(args.source)
    dest_folder = Path(args.dest)

    # Переконуємось, що шляхи існують
    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f'Source folder {source_folder} does not exist or is not a directory.')
        return
    if not dest_folder.exists():
        dest_folder.mkdir(parents=True, exist_ok=True)

    # Запускаємо асинхронну обробку
    asyncio.run(read_folder(source_folder, dest_folder))

if __name__ == '__main__':
    main()
