# solution/

This is the layer the student edits in their fork.

The buggy code lives in `app/`. To submit a fix:

1. Fork the repo.
2. Edit files in `app/` to fix the bugs you find.
3. Commit, push, and tag a new semver (`vX.Y.Z`). GitHub Actions builds and pushes your image to GHCR.
4. From the hardmode CLI: `hardmode session submit`.

This `solution/` directory is reserved for future course modes where the student's fix is overlaid on the original sources without modifying them. For this course, edit `app/` directly.
