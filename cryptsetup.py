Help options:
  -?, --help                            Show this help message
      --usage                           Display brief usage
  -V, --version                         Print package version
      --active-name=STRING              Override device autodetection of dm
                                        device to be reencrypted
      --align-payload=SECTORS           Align payload at <n> sector boundaries
                                        - for luksFormat
      --allow-discards                  Allow discards (aka TRIM) requests for
                                        device
  -q, --batch-mode                      Do not ask for confirmation
      --cancel-deferred                 Cancel a previously set deferred
                                        device removal
  -c, --cipher=STRING                   The cipher used to encrypt the disk
                                        (see /proc/crypto)
      --debug                           Show debug messages
      --debug-json                      Show debug messages including JSON
                                        metadata
      --deferred                        Device removal is deferred until the
                                        last user closes it
      --device-size=bytes               Use only specified device size (ignore
                                        rest of device). DANGEROUS!
      --decrypt                         Decrypt LUKS2 device (remove
                                        encryption).
      --disable-external-tokens         Disable loading of external LUKS2
                                        token plugins
      --disable-keyring                 Disable loading volume keys via kernel
                                        keyring
      --disable-locks                   Disable locking of on-disk metadata
      --disable-veracrypt               Do not scan for VeraCrypt compatible
                                        device
      --dump-json-metadata              Dump info in JSON format (LUKS2 only)
      --dump-volume-key                 Dump volume key instead of keyslots
                                        info
      --encrypt                         Encrypt LUKS2 device (in-place
                                        encryption).
      --force-password                  Disable password quality check (if
                                        enabled)
      --force-offline-reencrypt         Force offline LUKS2 reencryption and
                                        bypass active device detection.
  -h, --hash=STRING                     The hash used to create the encryption
                                        key from the passphrase
      --header=STRING                   Device or file with separated LUKS
                                        header
      --header-backup-file=STRING       File with LUKS header and keyslots
                                        backup
      --hotzone-size=bytes              Maximal reencryption hotzone size.
      --init-only                       Initialize LUKS2 reencryption in
                                        metadata only.
  -I, --integrity=STRING                Data integrity algorithm (LUKS2 only)
      --integrity-legacy-padding        Use inefficient legacy padding (old
                                        kernels)
      --integrity-no-journal            Disable journal for integrity device
      --integrity-no-wipe               Do not wipe device after format
  -i, --iter-time=msecs                 PBKDF iteration time for LUKS (in ms)
      --iv-large-sectors                Use IV counted in sector size (not in
                                        512 bytes)
      --json-file=STRING                Read or write the json from or to a
                                        file
      --keep-key                        Do not change volume key.
      --key-description=STRING          Key description
  -d, --key-file=STRING                 Read the key from a file
  -s, --key-size=BITS                   The size of the encryption key
  -S, --key-slot=INT                    Slot number for new key (default is
                                        first free)
      --keyfile-offset=bytes            Number of bytes to skip in keyfile
  -l, --keyfile-size=bytes              Limits the read from keyfile
      --keyslot-cipher=STRING           LUKS2 keyslot: The cipher used for
                                        keyslot encryption
      --keyslot-key-size=BITS           LUKS2 keyslot: The size of the
                                        encryption key
      --label=STRING                    Set label for the LUKS2 device
      --luks2-keyslots-size=bytes       LUKS2 header keyslots area size
      --luks2-metadata-size=bytes       LUKS2 header metadata area size
      --volume-key-file=STRING          Use the volume key from file.
      --new-keyfile=STRING              Read the key for a new slot from a file
      --new-key-slot=INT                Slot number for new key (default is
                                        first free)
      --new-keyfile-offset=bytes        Number of bytes to skip in newly added
                                        keyfile
      --new-keyfile-size=bytes          Limits the read from newly added
                                        keyfile
      --new-token-id=INT                Token number (default: any)
  -o, --offset=SECTORS                  The start offset in the backend device
      --pbkdf=STRING                    PBKDF algorithm (for LUKS2): argon2i,
                                        argon2id, pbkdf2
      --pbkdf-force-iterations=LONG     PBKDF iterations cost (forced,
                                        disables benchmark)
      --pbkdf-memory=kilobytes          PBKDF memory cost limit
      --pbkdf-parallel=threads          PBKDF parallel cost
      --perf-no_read_workqueue          Bypass dm-crypt workqueue and process
                                        read requests synchronously
      --perf-no_write_workqueue         Bypass dm-crypt workqueue and process
                                        write requests synchronously
      --perf-same_cpu_crypt             Use dm-crypt same_cpu_crypt
                                        performance compatibility option
      --perf-submit_from_crypt_cpus     Use dm-crypt submit_from_crypt_cpus
                                        performance compatibility option
      --persistent                      Set activation flags persistent for
                                        device
      --priority=STRING                 Keyslot priority: ignore, normal,
                                        prefer
      --progress-json                   Print progress data in json format
                                        (suitable for machine processing)
      --progress-frequency=secs         Progress line update (in seconds)
  -r, --readonly                        Create a readonly mapping
      --reduce-device-size=bytes        Reduce data device size (move data
                                        offset). DANGEROUS!
      --refresh                         Refresh (reactivate) device with new
                                        parameters
      --resilience=STRING               Reencryption hotzone resilience type
                                        (checksum,journal,none)
      --resilience-hash=STRING          Reencryption hotzone checksums hash
      --resume-only                     Resume initialized LUKS2 reencryption
                                        only.
      --sector-size=INT                 Encryption sector size (default: 512
                                        bytes)
      --serialize-memory-hard-pbkdf     Use global lock to serialize memory
                                        hard PBKDF (OOM workaround)
      --shared                          Share device with another
                                        non-overlapping crypt segment
  -b, --size=SECTORS                    The size of the device
  -p, --skip=SECTORS                    How many sectors of the encrypted data
                                        to skip at the beginning
      --subsystem=STRING                Set subsystem label for the LUKS2
                                        device
      --tcrypt-backup                   Use backup (secondary) TCRYPT header
      --tcrypt-hidden                   Use hidden header (hidden TCRYPT
                                        device)
      --tcrypt-system                   Device is system TCRYPT drive (with
                                        bootloader)
      --test-args                       Do not run action, just validate all
                                        command line parameters
      --test-passphrase                 Do not activate device, just check
                                        passphrase
  -t, --timeout=secs                    Timeout for interactive passphrase
                                        prompt (in seconds)
      --token-id=INT                    Token number (default: any)
      --token-only                      Do not ask for passphrase if
                                        activation by token fails
      --token-replace                   Replace the current token
      --token-type=STRING               Restrict allowed token types used to
                                        retrieve LUKS2 key
  -T, --tries=INT                       How often the input of the passphrase
                                        can be retried
  -M, --type=STRING                     Type of device metadata: luks, luks1,
                                        luks2, plain, loopaes, tcrypt, bitlk
      --unbound                         Create or dump unbound LUKS2 keyslot
                                        (unassigned to data segment) or LUKS2
                                        token (unassigned to keyslot)
      --use-random                      Use /dev/random for generating volume
                                        key
      --use-urandom                     Use /dev/urandom for generating volume
                                        key
      --uuid=STRING                     UUID for device to use
      --veracrypt                       Scan also for VeraCrypt compatible
                                        device
      --veracrypt-pim=INT               Personal Iteration Multiplier for
                                        VeraCrypt compatible device
      --veracrypt-query-pim             Query Personal Iteration Multiplier
                                        for VeraCrypt compatible device
  -v, --verbose                         Shows more detailed error messages
  -y, --verify-passphrase               Verifies the passphrase by asking for
                                        it twice
  -B, --block-size=MiB                  Reencryption block size
  -N, --new                             Create new header on not encrypted
                                        device
      --use-directio                    Use direct-io when accessing devices
      --use-fsync                       Use fsync after each block
      --write-log                       Update log file after every block
      --dump-master-key                 Alias for --dump-volume-key
      --master-key-file=STRING          Alias for --dump-volume-key-file

<action> is one of:
	open <device> [--type <type>] [<name>] - open device as <name>
	close <name> - close device (remove mapping)
	resize <name> - resize active device
	status <name> - show device status
	benchmark [--cipher <cipher>] - benchmark cipher
	repair <device> - try to repair on-disk metadata
	reencrypt <device> - reencrypt LUKS2 device
	erase <device> - erase all keyslots (remove encryption key)
	convert <device> - convert LUKS from/to LUKS2 format
	config <device> - set permanent configuration options for LUKS2
	luksFormat <device> [<new key file>] - formats a LUKS device
	luksAddKey <device> [<new key file>] - add key to LUKS device
	luksRemoveKey <device> [<key file>] - removes supplied key or key file from LUKS device
	luksChangeKey <device> [<key file>] - changes supplied key or key file of LUKS device
	luksConvertKey <device> [<key file>] - converts a key to new pbkdf parameters
	luksKillSlot <device> <key slot> - wipes key with number <key slot> from LUKS device
	luksUUID <device> - print UUID of LUKS device
	isLuks <device> - tests <device> for LUKS partition header
	luksDump <device> - dump LUKS partition information
	tcryptDump <device> - dump TCRYPT device information
	bitlkDump <device> - dump BITLK device information
	fvault2Dump <device> - dump FVAULT2 device information
	luksSuspend <device> - Suspend LUKS device and wipe key (all IOs are frozen)
	luksResume <device> - Resume suspended LUKS device
	luksHeaderBackup <device> - Backup LUKS device header and keyslots
	luksHeaderRestore <device> - Restore LUKS device header and keyslots
	token <add|remove|import|export> <device> - Manipulate LUKS2 tokens

You can also use old <action> syntax aliases:
	open: create (plainOpen), luksOpen, loopaesOpen, tcryptOpen, bitlkOpen, fvault2Open
	close: remove (plainClose), luksClose, loopaesClose, tcryptClose, bitlkClose, fvault2Close

<name> is the device to create under /dev/mapper
<device> is the encrypted device
<key slot> is the LUKS key slot number to modify
<key file> optional key file for the new key for luksAddKey action

Default compiled-in metadata format is LUKS2 (for luksFormat action).

LUKS2 external token plugin support is compiled-in.
LUKS2 external token plugin path: /lib/x86_64-linux-gnu/cryptsetup.

Default compiled-in key and passphrase parameters:
	Maximum keyfile size: 8192kB, Maximum interactive passphrase length 512 (characters)
Default PBKDF for LUKS1: pbkdf2, iteration time: 2000 (ms)
Default PBKDF for LUKS2: argon2id
	Iteration time: 2000, Memory required: 1048576kB, Parallel threads: 4

Default compiled-in device cipher parameters:
	loop-AES: aes, Key 256 bits
	plain: aes-cbc-essiv:sha256, Key: 256 bits, Password hashing: ripemd160
	LUKS: aes-xts-plain64, Key: 256 bits, LUKS header hashing: sha256, RNG: /dev/urandom
	LUKS: Default keysize with XTS mode (two internal keys) will be doubled.
