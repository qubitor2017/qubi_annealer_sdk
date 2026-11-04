# Publishing this SDK to GitHub

Recommended repository: `https://github.com/qubitor2017/qubitor-sdk`

Create an empty GitHub repository named `qubitor-sdk` under the Qubitor account. Do not initialise it with a README, licence or `.gitignore`, because those files are already included in this package.

From the extracted `qubitor-sdk-1.1.0` directory:

```bash
git init
git branch -M main
git add .
git commit -m "Release Qubitor SDK 1.1.0"
git remote add origin https://github.com/qubitor2017/qubitor-sdk.git
git push -u origin main
```

Then create a version tag and push it:

```bash
git tag -a v1.1.0 -m "Qubitor SDK v1.1.0"
git push origin v1.1.0
```

On GitHub, open Releases → Draft a new release, select tag `v1.1.0`, and attach `QUBITOR_SDK_1.1.0.zip` as a release asset. The website's Download Latest Release link opens the GitHub Releases page.

Before making the repository public, approve the proprietary SDK licence/EULA and verify that the repository contains no FPGA RTL, XDC, Vivado project, bitstream, internal firmware or other confidential hardware files.
