import sys
import interpreter

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gyri.py <filename>.gyri")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, "r") as f:
        raw = f.read().strip()
    
    interpreter.run(raw)