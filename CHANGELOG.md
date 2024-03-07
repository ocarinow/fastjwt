# CHANGELOG



## v0.4.0 (2024-03-07)

### Cicd

* [FIX][CI] Enable conditional execution of the deploy job ([`426a00c`](https://github.com/ocarinow/fastjwt/commit/426a00cf4c22eb57440414ea80c929c8ceaf81ef))

* [REFACTO][CI] Add CI/CD workflows for documentation, publishing, releasing, and testing ([`5f5e792`](https://github.com/ocarinow/fastjwt/commit/5f5e7929250cd9563603fda9faabaaa134f1e001))

* [CI] Add release task to Taskfile.yml ([`d669de4`](https://github.com/ocarinow/fastjwt/commit/d669de4020f21da8df187eb9bc2e7c6a8a252851))

* [CI] Update pre-commit hooks configuration ([`dc3be55`](https://github.com/ocarinow/fastjwt/commit/dc3be55d8f839e558af075f1ae11d4df9e2a8245))

### Configuration

* [FIX][CONFIG](tasks) Update Taskfile.yml to use Poetry for running flake8 and interrogate commands ([`823c631`](https://github.com/ocarinow/fastjwt/commit/823c6317ab01bad7a20f8e0b54d9bd5bcf033855))

* [CONFIG] Add setup tasks and generate badges ([`0ebc2a9`](https://github.com/ocarinow/fastjwt/commit/0ebc2a96a9394ca78d0dbf41992020567a2840ac))

* [CONFIG](tasks) Update release command in Taskfile.yml ([`a9fa8bf`](https://github.com/ocarinow/fastjwt/commit/a9fa8bf831318e2d282ae3502f47f4d89f73c744))

* [CONFIG](tasks) Add badges and update task descriptions ([`36e1383`](https://github.com/ocarinow/fastjwt/commit/36e138302c7578e3226090688ab8640d33eac167))

* [CONFIG] Add badge generation tasks ([`adb87e8`](https://github.com/ocarinow/fastjwt/commit/adb87e801b960eb5d520062d2ba2523e3d3a82fd))

* [CONFIG] Update release task in Taskfile.yml ([`da88fe7`](https://github.com/ocarinow/fastjwt/commit/da88fe70ad414666c0f105c13f1c62100678af98))

* [CONFIG] Add commit_parser_options to pyproject.toml ([`ce81c7c`](https://github.com/ocarinow/fastjwt/commit/ce81c7cc96b7b42e5f13b1385c73bf26e26846bc))

* [CONFIG] Update flake8 configuration ([`f8cf1c9`](https://github.com/ocarinow/fastjwt/commit/f8cf1c932782fa8ac9571ba9b2475b1ffc20b310))

* [CONFIG] Update dependencies in pyproject.toml ([`99e21d7`](https://github.com/ocarinow/fastjwt/commit/99e21d71074a062bc959bdf1be45cb3829a8d3be))

* [CONFIG] Update .gitignore to exclude all files in the &#39;reports&#39; directory ([`2bb53d7`](https://github.com/ocarinow/fastjwt/commit/2bb53d7a2c371d10e1a41da6f20b068b74951e4a))

* [CONFIG] Update dependencies in pyproject.toml ([`30e6e1f`](https://github.com/ocarinow/fastjwt/commit/30e6e1f33085d01d36919753cab330480783b784))

### Diff

* [RM] Remove coverage, docstr, flake8, and tests badges ([`1e70fbf`](https://github.com/ocarinow/fastjwt/commit/1e70fbfb742fd97565000223fdbb41a6a8fac1cc))

* [RM] Remove unused configuration files ([`1a46211`](https://github.com/ocarinow/fastjwt/commit/1a462118e6dd449fa59f2ef68495d00e40e53938))

### Documentation

* [DOC] Add new pages to navigation ([`201ef41`](https://github.com/ocarinow/fastjwt/commit/201ef4169ac22a120d41d7e8a48056697ad04b32))

* [DOC] Add documentation for aliases and API ([`40c018a`](https://github.com/ocarinow/fastjwt/commit/40c018ae3c4f5bc4ff13765250fc10dbdcddca1f))

* [DOC] Refactor docstrings ([`30e2646`](https://github.com/ocarinow/fastjwt/commit/30e2646c31f419e57b6255f71e0f287b804db309))

* [ADD][DOC] Add badges for pytest, coverage, and flake8 ([`bd7e78d`](https://github.com/ocarinow/fastjwt/commit/bd7e78ddf9d92fda1dd4a8df352bd64c8fadf79f))

* [DOC] Update Readme ([`f6755ca`](https://github.com/ocarinow/fastjwt/commit/f6755ca3fa4beedbb56826664110eb383394d811))

* [DOC] Clean base example ([`9a15572`](https://github.com/ocarinow/fastjwt/commit/9a15572c084be0084db295578671affd59c150bf))

### Feature

* [FEAT] Refactor callback setter to add less verbose aliases ([`8ef572d`](https://github.com/ocarinow/fastjwt/commit/8ef572db247849cc3cd138dabe02db04b64c2815))

* [FEAT] Update FastJWT dependency names ([`32393df`](https://github.com/ocarinow/fastjwt/commit/32393dfd5ecd1d329b0c70b3a024c74b94b3d677))

* [FEAT] Quick Dependency Accessors ([`5c22e23`](https://github.com/ocarinow/fastjwt/commit/5c22e237825ebf92c21a50174eb59463ddaa04da))

### Fix

* [CONFIG][FIX] Update assets to commit on release ([`81a5c3c`](https://github.com/ocarinow/fastjwt/commit/81a5c3c2c3b03af97c0892470b4cf9ae8ea3826c))

### Refactor

* [REFACTO] Refactor commit parser module for semantic release

This commit adds the commitparser.py module, which provides functionality for parsing commit messages in the semantic release format. The module includes a CommitTags enum, a CommitParser class, and various utility functions. This module will be used to enable semantic release in the project. ([`370d025`](https://github.com/ocarinow/fastjwt/commit/370d02549c532ab003e349e37541d6bbb2e3117d))

### Unknown

* Merge pull request #30 from ocarinow/dev

Bump version ([`fabcb71`](https://github.com/ocarinow/fastjwt/commit/fabcb712864d423de7022823f7bc9789b7549551))

* Merge pull request #29 from ocarinow/bump.major

Update dependencies, remove unused files, and refactor commit parser module ([`f53244b`](https://github.com/ocarinow/fastjwt/commit/f53244ba3dc1f5997e1741327e63112de08bf06d))

* docs: Add serve task to Taskfile.yml and update mkdocstrings configuration ([`a0fce7f`](https://github.com/ocarinow/fastjwt/commit/a0fce7f7960545e17b3cb554f4bfd54cf700822b))

* config: Add pytest-asyncio dependency ([`a2356f9`](https://github.com/ocarinow/fastjwt/commit/a2356f9a787c483186b61a72e2e737dda21e53a2))

* Merge branch &#39;main&#39; into bump.major ([`fa6bcc4`](https://github.com/ocarinow/fastjwt/commit/fa6bcc47aef4480975703e6982a401009164975f))

* [UPD][CONFIG] Update Taskfile.yml and add hooks and serve Taskfiles ([`cfa0b2d`](https://github.com/ocarinow/fastjwt/commit/cfa0b2ddf9ff2f05e35eaab9941996f3bee88870))


## v0.3.1 (2024-02-25)

### Cicd

* [FIX][CI] Update python-semantic-release version ([`21b113d`](https://github.com/ocarinow/fastjwt/commit/21b113d8668c6085999045d6153df66585fe4c67))

* [FIX][CI] Documentation workflow ([`0d29dcc`](https://github.com/ocarinow/fastjwt/commit/0d29dcc46cc79e1b250095d04cafe46ceb039cc2))

### Test

* [FIX][TEST] Fix missing iat in create_token test ([`a7a87df`](https://github.com/ocarinow/fastjwt/commit/a7a87df13b8a1337d481d9521c8dc1b6363facc5))

### Unknown

* Merge pull request #28 from ocarinow/dev

[FIX][CI] Update python-semantic-release version ([`ae2d29c`](https://github.com/ocarinow/fastjwt/commit/ae2d29cf0af48ffdc64939507b303993fdec7e2d))

* Merge pull request #27 from ocarinow/dev

Bump version ([`4fad3f7`](https://github.com/ocarinow/fastjwt/commit/4fad3f7626cd302227195f4cdbd9ff4a32508d73))

* Merge pull request #26 from ocarinow/upd/deps

[FEAT] Update dependencies and add fastapi to app dependencies ([`f1467eb`](https://github.com/ocarinow/fastjwt/commit/f1467eb9c52f7a7525cebeef63be6bae3e86d1d1))

* [UPD][CONFIG] Update dependencies and add fastapi to app dependencies ([`2ead1d0`](https://github.com/ocarinow/fastjwt/commit/2ead1d0e179a6e001f266765047ca37928990eb8))

* [UPD] Update from `pydantic.BaseSettings` to `pydantic_settings.BaseSettings` ([`de17cb8`](https://github.com/ocarinow/fastjwt/commit/de17cb82aaaa5109420a10a92924ac4c717d75b0))

* Merge pull request #24 from ocarinow/dev

Add Config section to documentation ([`87f2d90`](https://github.com/ocarinow/fastjwt/commit/87f2d9049d4c1552e0f61889d0f09594a27a62da))

* Merge pull request #23 from ocarinow/dev.mkdocs

Documentation ([`0a09189`](https://github.com/ocarinow/fastjwt/commit/0a09189e1d550a6ee940ba0437c717dd5d234454))

* add: lock requirements for mkdocs ([`3a255f2`](https://github.com/ocarinow/fastjwt/commit/3a255f267a0f8488a1105e6dd91fbff189ff8755))

* doc: add Config page ([`5e841d1`](https://github.com/ocarinow/fastjwt/commit/5e841d1519e81e5880fa7922a6f25fff672901a0))

* Merge pull request #22 from ocarinow/dev.doc

Bump 0.3.0 ([`22d6c71`](https://github.com/ocarinow/fastjwt/commit/22d6c71e16f879c9273326cd85b26a47a0a496f7))

* Merge branch &#39;main&#39; into dev.doc ([`a29fa91`](https://github.com/ocarinow/fastjwt/commit/a29fa910e836f3a4ac9843cee07ae5cf019942de))


## v0.3.0 (2023-03-15)

### Cicd

* [RM][CI] Install deps step in Release workflow ([`56a76fb`](https://github.com/ocarinow/fastjwt/commit/56a76fb7b4fa98321d303698d851c9885e8d5bb9))

* [FIX][CI] Force virtualenv in project for Release workflow ([`96e10ec`](https://github.com/ocarinow/fastjwt/commit/96e10ec96fffd6d1d78847d312a544fc2efbf5a2))

* [FIX][CI] Force poetry install on semantic release task ([`0591e80`](https://github.com/ocarinow/fastjwt/commit/0591e80e93373ed4d4194b249d092c7338875649))

* [FIX][CI] Pre commit semantic release command

Force `poetry run` for commands ([`14f7e22`](https://github.com/ocarinow/fastjwt/commit/14f7e227a448704d874059058d316223ba6a609c))

* [FIX][CI] Add fetch-depth to Release workflow ([`0196fc7`](https://github.com/ocarinow/fastjwt/commit/0196fc7b488e37a1c3e328592c434dab9df7711e))

* [FIX][CI] Launch Publish &amp; Doc on success ([`42fe4d7`](https://github.com/ocarinow/fastjwt/commit/42fe4d734050fdc8f847036c961fbb836efcb97a))

* [FIX][CI] Remove upload to release config ([`500be27`](https://github.com/ocarinow/fastjwt/commit/500be2785f3c10b5458eef6534f4eef0ec4289a6))

* [CI] MkDoc deploy on package publish ([`6261b67`](https://github.com/ocarinow/fastjwt/commit/6261b67e84faa536eacd8840fe825a5779441f60))

### Configuration

* [DOC][CONFIG] enable mkdoc code block annotations ([`1148788`](https://github.com/ocarinow/fastjwt/commit/114878808a78b8d3a4cd197975aa91329bdca047))

* [FIX][CONFIG] License typo ([`a81a73b`](https://github.com/ocarinow/fastjwt/commit/a81a73bf4e2bc0b45d0b4a4996b237e7e3c2e6e0))

### Diff

* [ADD] add missing `create_refresh_token` to FastJWTDeps ([`be3a83f`](https://github.com/ocarinow/fastjwt/commit/be3a83f937ca08bf01870ff28611f9e793ff8d7e))

* [ADD] mkdocs dist to .gitignore ([`2268d60`](https://github.com/ocarinow/fastjwt/commit/2268d600214e8ba0fddaa11731752da69d3e680f))

### Documentation

* [DOC] Add documentation workflow badge ([`4f9faa8`](https://github.com/ocarinow/fastjwt/commit/4f9faa88a455dfece76b28babd3d53d37eb3ee1e))

* [DOC] Add base docstring args for TokenPayload ([`b3c4533`](https://github.com/ocarinow/fastjwt/commit/b3c45335383964e2b6824c0f940ac52fc236f07a))

* [DOC] Add type hints documentation ([`bc322ab`](https://github.com/ocarinow/fastjwt/commit/bc322abb26182bc1ac1e1665587faf23e7edebbb))

* [DOC] add documentation for claims ([`dbf7f71`](https://github.com/ocarinow/fastjwt/commit/dbf7f71a18f55caa9ef88001e04b879416a08db1))

* [DOC] Add documentation for error handling ([`d52edb6`](https://github.com/ocarinow/fastjwt/commit/d52edb653f61aec7e6ecf3757e5b3c0d5b1827ea))

* [DOC] add documentation for FastJWTDeps ([`a102332`](https://github.com/ocarinow/fastjwt/commit/a1023323ebba1648bf1fa8d808c3a1549a1ae282))

* [DOC] Add documentation for dependencies ([`3458bdb`](https://github.com/ocarinow/fastjwt/commit/3458bdb8da11f3cd04de063a6f0ca27724753721))

* [DOC] Add documentation pages ([`4cb1a14`](https://github.com/ocarinow/fastjwt/commit/4cb1a14baba3b1391bbbd62da7d0b76adbaa88b7))

* [DOC] Format mk files ([`a5e377c`](https://github.com/ocarinow/fastjwt/commit/a5e377c294be16bfff35fb086c61f2d400c4f40d))

* [DOC] Docstrings for implicit refresh mechanism ([`4d5c29a`](https://github.com/ocarinow/fastjwt/commit/4d5c29ada2775225c1850f85498fd93c32969331))

* [ADD][DOC] Docstrings for additional `TokenPayload` properties ([`cc05713`](https://github.com/ocarinow/fastjwt/commit/cc057138f1ad53f7e1885a02738b102f96fa44e5))

* [DOC] Fix badges in README.md ([`1d7774e`](https://github.com/ocarinow/fastjwt/commit/1d7774e2ffcad27199a8fc43e7a520d9294d92ca))

* [DOC] Add docstrings ([`3d98c45`](https://github.com/ocarinow/fastjwt/commit/3d98c453dedee4c1dadbc8331cb2fd3dce103fc9))

* [DOC] enable mermaid in doc ([`c5754ec`](https://github.com/ocarinow/fastjwt/commit/c5754ec7cfb8475c20c31360d0d23adfc262ab93))

* [DOC] Add semver documentation ([`31b5311`](https://github.com/ocarinow/fastjwt/commit/31b5311fbd9c7c3a324fecc2a39ed85af916baab))

### Feature

* [FEAT] Implicit refresh middleware ([`97b54ff`](https://github.com/ocarinow/fastjwt/commit/97b54ff619c73c04605da27cb17e05ecb05cdb4b))

* [ADD][FEAT] FastJWT under MIT Licence ([`2b4bb8a`](https://github.com/ocarinow/fastjwt/commit/2b4bb8a7be90be54bd6593d3ff6e3ef9ded1e72b))

* [FEAT] Add quick imports for main objects ([`88144d6`](https://github.com/ocarinow/fastjwt/commit/88144d640b7de620e5a5b61bcea2f8b6424fa978))

* [FEAT](subject) Allow user defined subject fetching callback

Given a user defined callback `(str) -&gt; Model` FastJWT provides a `get_current_subject` method to fetch and serialize user as a dependency ([`3b87d4e`](https://github.com/ocarinow/fastjwt/commit/3b87d4e5bdbbc4cd2afc88ce69f55c1e9601e609))

* [FEAT](revoked) Add revoked token handling

Enable checks for revoked tokens through user defined callback ([`f2ffa56`](https://github.com/ocarinow/fastjwt/commit/f2ffa5619116143892a60a5c2221394dc23d6b37))

* [FEAT](error) Move token deps as properties

Set the token dependencies as non parametrizable properties to follow fastapi syntax. New properties
- `FastJWT.fresh_token_required`
- `FastJWT.access_token_required`
- `FastJWT.refresh_token_required` ([`e2cb3a1`](https://github.com/ocarinow/fastjwt/commit/e2cb3a15c3ccc47f8d5399b32f90844a234d73d6))

* [FEAT] Error Handling ([`1dbeb47`](https://github.com/ocarinow/fastjwt/commit/1dbeb477e1746a6d0c3dbdafdee1cb22d83d780e))

### Fix

* [FIX] Default CallbackHandler `ignore_errors` argument to False ([`36e4664`](https://github.com/ocarinow/fastjwt/commit/36e4664db0771c0b7557d8bcebcb005c1b6819e8))

* [FIX] Exception inheritance ([`298c401`](https://github.com/ocarinow/fastjwt/commit/298c4011a1d53943bee47d283427886fa04b2d0e))

### Test

* [RM][TEST] Remove unused imports ([`468449b`](https://github.com/ocarinow/fastjwt/commit/468449bde03faef6ba7f60865de7fcf934950f51))

* [TEST] Add tests for error &amp; callbcak handlers ([`b21f550`](https://github.com/ocarinow/fastjwt/commit/b21f5508a5a2cb80da990eb40a14e17786de5602))

* [TEST] Excpect specific MissingCSRFTokenError ([`7c0cf0b`](https://github.com/ocarinow/fastjwt/commit/7c0cf0ba3b003c36632fb2ca3e82ff640d8ff147))

* [FIX][TEST] Fix tests with `FastJWT.token_required` coroutine generator ([`4a50065`](https://github.com/ocarinow/fastjwt/commit/4a50065fa7fc9b85c3213e1739867ec1fc53944b))

* [RM][TEST] Remove debug prints in tests ([`7d93cc4`](https://github.com/ocarinow/fastjwt/commit/7d93cc4ee09b28ab3cf62a75f385dccad0e465d2))

* [TEST] use MissingTokenError ([`d80a304`](https://github.com/ocarinow/fastjwt/commit/d80a3046ff48c556bf6d245ddf0d0b03906e0950))

### Unknown

* Merge pull request #21 from ocarinow/dev.doc

[RM][CI] Install deps step in Release workflow ([`53fbe9e`](https://github.com/ocarinow/fastjwt/commit/53fbe9e9c9890324ebe6107d28996abf35c23cb6))

* Merge pull request #20 from ocarinow/dev.doc

Poetry setup in Release CI workflow ([`214c297`](https://github.com/ocarinow/fastjwt/commit/214c2970fcbb16ba5fe8128674c395814e837f33))

* Merge pull request #19 from ocarinow/dev.doc

[FIX][CI] Pre commit semantic release command ([`2c35f5a`](https://github.com/ocarinow/fastjwt/commit/2c35f5a6a1ea6ead76c5ef4b53420fdaa4ba9785))

* Merge pull request #18 from ocarinow/dev.doc

[FIX][CI] Add fetch-depth to Release workflow ([`7227d23`](https://github.com/ocarinow/fastjwt/commit/7227d23e001f0e37a13307c61427cf4d79b322e1))

* Merge pull request #17 from ocarinow/dev

Fix CI issue ([`5be7785`](https://github.com/ocarinow/fastjwt/commit/5be77853462137b52ba2b5a0a5e82b75783f8612))

* Merge pull request #16 from ocarinow/dev.doc

Fix CI by disabling upload_to_release ([`42c84eb`](https://github.com/ocarinow/fastjwt/commit/42c84eb63d39fcf9b4e5dfe7d99974b906661980))

* Merge pull request #15 from ocarinow/dev.doc

[FIX][CI] Remove upload to release config ([`22cd1b4`](https://github.com/ocarinow/fastjwt/commit/22cd1b4edee84898f9c8b59ce31dcb4aad89a6d6))

* Merge pull request #14 from ocarinow/dev

Add new features ([`5de6c1d`](https://github.com/ocarinow/fastjwt/commit/5de6c1ddf4f492cf0004744003f0ca7706c5c304))

* Merge pull request #13 from ocarinow/dev.doc

Add new features ([`46cd5f6`](https://github.com/ocarinow/fastjwt/commit/46cd5f650cce885513743ddc306db4561de54331))

* [UPD][DOC] Readme ([`a430446`](https://github.com/ocarinow/fastjwt/commit/a43044639e8a0d3bfc75ab5c98f8c64a89ba7848))


## v0.2.1 (2023-03-11)

### Cicd

* [CI] Remove beautify step ([`39c2ad0`](https://github.com/ocarinow/fastjwt/commit/39c2ad0a2f4d0bca0c47c3a856551b92c58199bf))

* [CI] Force tests only on PR@dev ([`b2b812d`](https://github.com/ocarinow/fastjwt/commit/b2b812dd8a0cec802afd7b0a0e770322de386c2a))

* [CI] Add set poetry to release workflow ([`9a6e17e`](https://github.com/ocarinow/fastjwt/commit/9a6e17eb5382c48515c27e16a0eed918c7dfd46f))

* [CI] Set publish workflow on Release success ([`9b2f2bd`](https://github.com/ocarinow/fastjwt/commit/9b2f2bd56ba1e1dd815caf1cb30174903c0e1ece))

* [CI] Use Set Poetry step in Release ([`c33701f`](https://github.com/ocarinow/fastjwt/commit/c33701f94b9d2c37fbe89a2247d4ef5bec2f96f7))

* [CI] Disable flake8 on test workflow ([`4ceeee0`](https://github.com/ocarinow/fastjwt/commit/4ceeee050053b8511529fec55d0375bbbafea137))

* [FIX][CI] Use `poetry run` to activate env ([`a8a2296`](https://github.com/ocarinow/fastjwt/commit/a8a2296f4cd909c00919805d021b6ca113a8f2b1))

* [CI] Fix typing for python3.9 ([`65b06db`](https://github.com/ocarinow/fastjwt/commit/65b06dbb53bcbd0b60afc4d4151b27333c1a60e0))

* [FIX][CI] Fix Test GHA for 3.9 ([`00de0f7`](https://github.com/ocarinow/fastjwt/commit/00de0f7ce9185c005b91b3042516a9c587c991d2))

* [CI] Run test on PR on dev ([`7e3c3ef`](https://github.com/ocarinow/fastjwt/commit/7e3c3efea88939889da321116aaae28a7c88ca90))

* [CI] Add github actions ([`3846279`](https://github.com/ocarinow/fastjwt/commit/38462796594d7e72229a72781f9f10765472c0e2))

* [CI] Add requirements.txt ([`525aabd`](https://github.com/ocarinow/fastjwt/commit/525aabdc1bb7651e3edb4f7af0fceea29b4a2933))

* [CI] Sepcify packages to include in toml ([`545c6c0`](https://github.com/ocarinow/fastjwt/commit/545c6c0cdf3a457fc24875030ea9d32dd583c2cd))

* [CI] Add commit parser ([`f6c6c46`](https://github.com/ocarinow/fastjwt/commit/f6c6c463a8cafa9726ced1c083ccf50c686cea27))

### Configuration

* [CONFIG] Update config ([`0cbe9be`](https://github.com/ocarinow/fastjwt/commit/0cbe9be616068b862d39ab5d0fdd5a3d773d47fa))

* [CONFIG] pytest config ([`cd17af5`](https://github.com/ocarinow/fastjwt/commit/cd17af52037699eb07d1e77bfa6995e7a8a72097))

### Diff

* [ADD] Readme.md ([`8c86b3d`](https://github.com/ocarinow/fastjwt/commit/8c86b3d104a0a991b4576af05661585d23d70877))

* [RM] bad doc ([`2268360`](https://github.com/ocarinow/fastjwt/commit/2268360a8a2900922394abe530604f3a7c50a08f))

* [ADD] requirements ([`2f2811d`](https://github.com/ocarinow/fastjwt/commit/2f2811da265428affd810ddb1396b197d055d82c))

* [RM] debug prints ([`954281e`](https://github.com/ocarinow/fastjwt/commit/954281ea1b776dc092fef52781e02a08dfecd01d))

* [RM] Old quick imports ([`284f74c`](https://github.com/ocarinow/fastjwt/commit/284f74cca0ad6a83eef9a53e7a70ab56c394e449))

* [ADD] Encode/decode warppers ([`f0fb8d1`](https://github.com/ocarinow/fastjwt/commit/f0fb8d1e4efbaf9641f4e42b8c2024d9f40fdee8))

* [ADD] Exceptions ([`8346093`](https://github.com/ocarinow/fastjwt/commit/83460931054f6378cdaff072593e7c2f965b1c6f))

* [ADD] type hints ([`6890ddc`](https://github.com/ocarinow/fastjwt/commit/6890ddc2110bf0263206928f2ee0b4c008ccd640))

* [ADD] utils functions ([`6e70e5b`](https://github.com/ocarinow/fastjwt/commit/6e70e5ba687ed1068f6ec5fbfba6f1e256188ef0))

* [RM] Remove old api ([`c93f00d`](https://github.com/ocarinow/fastjwt/commit/c93f00da1ecc16839abd8c8e21b1885ce9f355a0))

* [ADD] shell script to test jwt plugin behavior ([`dd9f929`](https://github.com/ocarinow/fastjwt/commit/dd9f929c8317baca7badea802930263a7bc32899))

* [ADD] Add token blacklisting to `base` example ([`4caaa7d`](https://github.com/ocarinow/fastjwt/commit/4caaa7d6f067eac86b2f39e48726c91dfe7b8cd3))

* [ADD](examples) Create base example ([`48c488a`](https://github.com/ocarinow/fastjwt/commit/48c488aff296393bae6e85b7ba6c797675f74986))

* [ADD] Add repo structure ([`e738102`](https://github.com/ocarinow/fastjwt/commit/e738102c221f2e04389f7ac319cb282f7e06b3bf))

### Documentation

* [DOC] improve documentation ([`3126724`](https://github.com/ocarinow/fastjwt/commit/31267246ebee237881ef680562ce69d24f3af1c2))

* [DOC] improve documentation ([`7f6c3eb`](https://github.com/ocarinow/fastjwt/commit/7f6c3eb6d09e43c45a753a854c12723c68925498))

* [DOC] Add mkdocs ([`4ca2833`](https://github.com/ocarinow/fastjwt/commit/4ca28338f653c1303308aa0da47aa9dfe13f7e27))

* [ADD][DOC] Add MkDoc base ([`2eede25`](https://github.com/ocarinow/fastjwt/commit/2eede2519847a5d46b6e9d1cae79fbb319c37552))

* [ADD][DOC] Add mkdoc deps ([`3d4a727`](https://github.com/ocarinow/fastjwt/commit/3d4a72738776ae34e3cf7b0e942eb11f8952baff))

* [DOC] Add MkDoc ([`6f0256b`](https://github.com/ocarinow/fastjwt/commit/6f0256b9aa80605d8baa0a6aa97045b6612c19b1))

* [DOC] Coverage badge ([`5348ca4`](https://github.com/ocarinow/fastjwt/commit/5348ca4c23abcdc2ba05f0453454467e4a2bd6ce))

* [DOC] Add docstring for public methods/functions ([`a7cb52f`](https://github.com/ocarinow/fastjwt/commit/a7cb52f14b5ee580cd97910bc211cd4f1702da30))

* [DOC] Add reports ([`8cf5743`](https://github.com/ocarinow/fastjwt/commit/8cf5743c34dd5fee0322526561af95eac2f865cb))

* [DOC] Document release ([`688e009`](https://github.com/ocarinow/fastjwt/commit/688e00948eb77fd701b9d778e942fa515e9a0240))

* [DOC](examples) Add comments in `base` example ([`9d1db65`](https://github.com/ocarinow/fastjwt/commit/9d1db65ab50b5c49dd72f35f0d8a3e0039358f0f))

### Feature

* [FEAT] Add dependency and callback handler ([`ec2b7a4`](https://github.com/ocarinow/fastjwt/commit/ec2b7a4de2827644b8686271b667c031506dc3d7))

* [DOC][FEAT] Force bump ([`5767404`](https://github.com/ocarinow/fastjwt/commit/5767404e28b37fa089187098da9b6038f766c0ad))

* [FEAT] FastJWT object and first protection deps ([`9e2eb03`](https://github.com/ocarinow/fastjwt/commit/9e2eb03f737dfe0dbe1058c61e5dfd951882ab06))

* [FEAT] TokenPayload &amp; RequestToken models ([`6d6fe94`](https://github.com/ocarinow/fastjwt/commit/6d6fe94f826e05156d7b6fd59884b776b93a1a9c))

* [FEAT] Add token getter from request ([`ca7dd9f`](https://github.com/ocarinow/fastjwt/commit/ca7dd9f7b0a5e1cc7bd1acbdd27e02d5e0f663d4))

* [FEAT] Use `pydantic.BaseSettings` for Config ([`3311811`](https://github.com/ocarinow/fastjwt/commit/331181197943742a9ff17b4f09848ecee16e81e0))

* [FEAT] Check for token in blacklist ([`188e278`](https://github.com/ocarinow/fastjwt/commit/188e2788284382cd89d28a2862d30c6b5b79bb32))

* [FEAT](jwt) FastJWT object for auth management ([`b2da6af`](https://github.com/ocarinow/fastjwt/commit/b2da6afa98230d8c5cc5fb91f636f2269bee38ac))

### Fix

* [FIX] dependency method typing ([`2db54f4`](https://github.com/ocarinow/fastjwt/commit/2db54f49a82bc8927729d206748467d84818868a))

* [FIX] Fix type hinting from iterable to sequence ([`87c89fe`](https://github.com/ocarinow/fastjwt/commit/87c89feb51e732a0b75bac8a399f9df3f9237e6e))

* [FIX] Make &#34;iat&#34; claim int ([`a9676eb`](https://github.com/ocarinow/fastjwt/commit/a9676eb0140bcb93d83ffab9b4c8a96031822e02))

* [FIX] Missing &#34;sub&#34; in reserved claims ([`93bb39c`](https://github.com/ocarinow/fastjwt/commit/93bb39c7df44c980290f60a3b5c5bf0dc71797c9))

* [FIX] TokenLocations &amp; HTTPMethods sequence typing ([`f7640b8`](https://github.com/ocarinow/fastjwt/commit/f7640b84a45402388b7210deefbeea48a27e5698))

* [FIX] FastJWTConfig hidden arguments ([`3f236eb`](https://github.com/ocarinow/fastjwt/commit/3f236ebe09999d4d44e4554fee3f6fec0b74673c))

### Refactor

* [REFACTO] Remove unused imports ([`76bd4d7`](https://github.com/ocarinow/fastjwt/commit/76bd4d79f993f77bbc4c7319a0de4e1e83033a7b))

### Test

* [TEST] Add tests for FastJWT object ([`d12f23f`](https://github.com/ocarinow/fastjwt/commit/d12f23fe5412c1f972b9c6539269e23eef584da5))

* [TEST] Add test for model&#39;s methods ([`fd4c4d6`](https://github.com/ocarinow/fastjwt/commit/fd4c4d6ebe0bda0242845d24276089a7330c4ba0))

* [TEST] Add tests for encode/decode behavior ([`04395b8`](https://github.com/ocarinow/fastjwt/commit/04395b8cb4d769c85b1142b0a1b09db18b867d69))

* [TEST] Add utils basic tests ([`83fa88f`](https://github.com/ocarinow/fastjwt/commit/83fa88ffcba5ee91c7ef26ff2e5a63bcee5fb418))

* [TEST] Add tests for config object ([`ca4b816`](https://github.com/ocarinow/fastjwt/commit/ca4b816f9c4218b7976264da6cbe3155e38424a0))

* [TEST] Add test for fastjwt.core uncovered branches ([`4d49455`](https://github.com/ocarinow/fastjwt/commit/4d49455534776d5d2a153773e39fd3b7a7abd8a2))

* [TEST] Add test for token getters in request ([`f366da1`](https://github.com/ocarinow/fastjwt/commit/f366da1bbce5046b3a035e2aaac3af0e1835a48f))

### Unknown

* Merge pull request #12 from ocarinow/dev

Publish 0.2.0 ([`7333a0d`](https://github.com/ocarinow/fastjwt/commit/7333a0d8b85936c0375a4e4fd1798cee4c4c3664))

* Merge pull request #11 from ocarinow/dev.doc

Bump to v0.2.0 ([`557736e`](https://github.com/ocarinow/fastjwt/commit/557736e5ba2cbbeeafb5968fa63a72261e09d710))

* Merge pull request #10 from ocarinow/dev

[DOC][FEAT] Manual Bump ([`cdf7f25`](https://github.com/ocarinow/fastjwt/commit/cdf7f2555cee70e8ac45e4368d283c7488eb5e0c))

* Merge pull request #9 from ocarinow/dev.doc

[DOC][FEAT] Force bump ([`d6374c0`](https://github.com/ocarinow/fastjwt/commit/d6374c052336c1182e2ce2f329fded94bb84c086))

* Merge pull request #6 from ocarinow/dev

[CI] release &amp; publish ([`a8afb44`](https://github.com/ocarinow/fastjwt/commit/a8afb443f14559dac8bfa8bd45611c0ecbb16a99))

* Merge pull request #5 from ocarinow/dev.doc

[CI] Configure CI ([`4ff334c`](https://github.com/ocarinow/fastjwt/commit/4ff334c75483166d685046d532d6dcd4cca319fa))

* Merge pull request #4 from ocarinow/dev

Try first release &amp; publish ([`d4039e8`](https://github.com/ocarinow/fastjwt/commit/d4039e85364112eff09a8afd81679c0277707e83))

* Merge pull request #3 from ocarinow/dev.doc

Add doc and update CI ([`87a75fb`](https://github.com/ocarinow/fastjwt/commit/87a75fbf215bb4152290d6c44907be64045e0f3e))

* Merge pull request #2 from ocarinow/dev.std

[CI] Add Test GHA on PR@dev ([`22d1167`](https://github.com/ocarinow/fastjwt/commit/22d11674d9e445f77aa0bfa01edc746cb3c877cc))

* Merge pull request #1 from ocarinow/dev.std

Refacto FastJWT API ([`775119a`](https://github.com/ocarinow/fastjwt/commit/775119aad91bd220608fcd1d2366c7a91dd3a609))

* Initial commit ([`9c1d6ec`](https://github.com/ocarinow/fastjwt/commit/9c1d6ecf8236b10e66db24ac74b6cfee884305dc))
