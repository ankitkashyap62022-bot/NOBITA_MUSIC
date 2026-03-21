import os
import glob

# ==========================================
# ☠️ ANU MATRIX PREMIUM AUTO-LOADER (FIXED) ☠️
# ==========================================

def __list_all_modules():
    work_dir = os.path.dirname(__file__)
    # 💎 DEEP SCAN: Scans direct files AND sub-folders automatically 💎
    mod_paths = glob.glob(work_dir + "/**/*.py", recursive=True)

    all_modules = []
    for f in mod_paths:
        if os.path.isfile(f) and f.endswith(".py") and not f.endswith("__init__.py"):
            # ☠️ THE FIX: Removed lstrip() to preserve the leading dot! ☠️
            rel_path = f.replace(work_dir, "")
            # Converting slashes to dots properly
            module_name = rel_path.replace("\\", ".").replace("/", ".")[:-3]
            all_modules.append(module_name)

    return all_modules

ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
