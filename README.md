# Lettermint Homebrew tap

This tap contains the macOS cask for the [Lettermint CLI](https://github.com/lettermint/lettermint-cli).

The first cask will arrive with the first signed stable release. After its pull request is merged:

```sh
brew install --cask lettermint/tap/lettermint
brew upgrade --cask lettermint
brew uninstall --cask lettermint
```

Each stable release proposes a cask change. Review the cask, release checks, and native Mac checks before a manual merge. Pre-releases and older releases must not replace the current cask. Require the branch to be up to date before merge.

For exact versions, manual installation, and security reports, see the CLI repository.
