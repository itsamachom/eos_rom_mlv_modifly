# Install FIRMWARE ADD-ON Thai-Menu — Canon 600D

Canon EOS 600D / Rebel T3i / Kiss X5 with Canon firmware **1.0.2 only**. ML-SETUP.FIR is the original ML installer, not a Canon firmware 1.0.2 update.

Choose **FIRST-INSTALL.zip** if ML has never been installed: it contains autoexec.bin, ML/ and ML-SETUP.FIR; no separate prior ML package is required. Choose **UPDATE.zip** for an existing working ML camera/card: no FIR is included. Source ZIP is for development, not card installation.

## First installation

Based on the included upstream INSTALL_UPSTREAM.txt. This release is Experimental; its first-install hardware behavior has not been tested by this project.

1. Verify Canon firmware 1.0.2 in the camera menu. Stop if it differs; use model-correct Canon information/files first, not the ML FIR as a Canon updater.
2. Back up the card, fully charge an original Canon battery, remove accessories and select Manual (M).
3. For first installation use a simple SD/SDHC card of 32 GB or less, as required by the upstream guide. After backing up, format it in the camera; formatting erases files.
4. Turn off the camera. Wait for card activity to stop and at least five seconds after opening the card door. Use a reader to extract FIRST-INSTALL.zip at the card root: autoexec.bin, ML/ and ML-SETUP.FIR must not be inside an extra folder.
5. Eject the card, insert it into the powered-off camera and turn on in M.
6. Use Canon Firmware Ver. > Firmware Update to run the included ML-SETUP.FIR.
7. At the green confirmation / "Please restart your camera." message, restart as instructed. Do not remain on that installer screen: the original installer counts down 60 seconds towards uninstalling.
8. If there is an error, black screen or abnormal card LED activity, stop. Do not repeatedly flash or substitute random files. Read upstream Troubleshooting and report the symptoms.
9. After restart, press Delete to open the menu, then Setup (+) > Version > Thai-Menu. Verify the downloaded version and test ordinary photos before relying on it.
10. Keep any generated ML/LOGS/ROM*.BIN backups private on your computer; do not publish Canon ROM dumps.

## Existing ML camera and bootable card

Back up autoexec.bin and ML/. With the camera off, use a reader to replace autoexec.bin and the complete ML/ directory from UPDATE.zip at the card root. No format or repeat Firmware Update is needed for this menu update. Check the version after boot.

A new card may require boot preparation even when the camera already has ML; see "Installing Magic Lantern on other cards" upstream. Never boot an ML-bootable card without a working autoexec.bin. Restore both backed-up runtime components to roll back; uninstalling the camera boot flag is a separate upstream procedure.

Project: https://itsamachom.github.io/eos_rom_mlv_modifly/
Developer: https://www.youtube.com/@Online2easy / https://www.facebook.com/online2easy / https://online2hobby.blogspot.com/

Preserve original credits/licenses. Independent Codex/LLM-assisted fork, not endorsed by Canon or Magic Lantern. Inherited dietlibc corresponding source remains unverified; see THIRD_PARTY_NOTICES.md and release/v3r2/PROVENANCE.md.
