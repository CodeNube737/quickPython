def cell_address(row, col):
    """Convert zero-based row, col to spreadsheet address, e.g. (0,0) -> 'A1'"""
    return chr(col + 65) + str(row + 1)

def toggle_reference(ref):
    # Toggle between A1 and $A$1
    if '$' in ref:
        return ref.replace('$', '')
    else:
        col = ref[0]
        row = ref[1:]
        return f"${col}${row}"