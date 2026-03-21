import os
import glob

# ==========================================
# ☠️ ANU MATRIX PREMIUM AUTO-LOADER ☠️
# ==========================================

def __list_all_modules():
    work_dir = os.path.dirname(__file__)
    # 💎 DEEP SCAN: Scans direct files AND sub-folders automatically 💎
    mod_paths = glob.glob(work_dir + "/**/*.py", recursive=True)

    all_modules = []
    for f in mod_paths:
        if os.path.isfile(f) and f.endswith(".py") and not f.endswith("__init__.py"):
            # ☠️ CLEAN PATH EXTRACTOR (No Crash Bugs) ☠️
            rel_path = f.replace(work_dir, "")
            # Removing leading slashes and converting to dot format
            module_name = rel_path.lstrip("\\/").replace("\\", ".").replace("/", ".")[:-3]
            all_modules.append(module_name)

    return all_modules

ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
