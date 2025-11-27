try:
    import colorama
    print("Colorama imported successfully!")
except ImportError as e:
    print("Import error:", e)
    import sys
    print("sys.path:", sys.path)
