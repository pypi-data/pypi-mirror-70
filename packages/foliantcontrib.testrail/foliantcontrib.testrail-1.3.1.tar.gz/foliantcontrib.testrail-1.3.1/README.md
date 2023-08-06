# TestRail cases downloader for Foliant

TestRail preprocessor collects test cases from TestRail project and adds to your testing procedure document.


## Installation

```shell
$ pip install foliantcontrib.testrail
```


## Config

To enable the preprocessor, add `testrail` to `preprocessors` section in the project config. The preprocessor has a number of options (best values are set by default where possible):

```yaml
preprocessors:
  - testrail:
    testrail_url: http://testrails.url                                                      \\ Required
    testrail_login: username                                                                \\ Required
    testrail_pass: password                                                                 \\ Required
    project_id: 35                                                                          \\ Required
    suite_ids:                                                                              \\ Optional
    section_ids:                                                                            \\ Optional
    exclude_suite_ids:                                                                      \\ Optional
    exclude_section_ids:                                                                    \\ Optional
    exclude_case_ids:                                                                       \\ Optional
    filename: test_cases.md                                                                 \\ Optional
    rewrite_src_files: false                                                                \\ Optional
    template_folder: case_templates                                                         \\ Optional
    img_folder: testrail_imgs                                                               \\ Optional
    move_imgs_from_text: false                                                              \\ Optional
    section_header: Testing program                                                         \\ Recommended
    std_table_header: Table with testing results                                            \\ Recommended
    std_table_column_headers: №; Priority; Platform; ID; Test case name; Result; Comment    \\ Recommended
    add_std_table: true                                                                     \\ Optional
    add_suite_headers: true                                                                 \\ Optional
    add_section_headers: true                                                               \\ Optional
    add_case_id_to_case_header: false                                                       \\ Optional
    add_case_id_to_std_table: false                                                         \\ Optional
    multi_param_name:                                                                       \\ Optional
    multi_param_select:                                                                     \\ Optional
    multi_param_select_type: any                                                            \\ Optional
    add_cases_without_multi_param: true                                                     \\ Optional
    add_multi_param_to_case_header: false                                                   \\ Optional
    add_multi_param_to_std_table: false                                                     \\ Optional
    checkbox_param_name:                                                                    \\ Optional
    checkbox_param_select_type: checked                                                     \\ Optional
    choose_priorities:                                                                      \\ Optional
    add_priority_to_case_header: false                                                      \\ Optional
    add_priority_to_std_table: false                                                        \\ Optional
    resolve_urls: true                                                                      \\ Optional
    screenshots_url: https://gitlab_repository.url                                          \\ Optional
    img_ext: .png                                                                           \\ Optional
    print_case_structure: true                                                              \\ For debugging
```

`testrail_url`
:   URL of TestRail deployed.

`testrail_login`
:   Your TestRail username.

`testrail_pass`
:   Your TestRail password.

`project_id`
:   TestRail project ID. You can find it in the project URL, for example http://testrails.url/index.php?/projects/overview/17 <-.

`suite_ids`
:   If you have several suites in your project, you can download test cases from certain suites. You can find suite ID in the URL again, for example http://testrails.url/index.php?/suites/view/63... <-.

`section_ids`
:   Also you can download any sections you want regardless of it's level. Just keep in mind that this setting overrides previous *suite_ids* (but if you set *suite_ids* and then *section_ids* from another suite, nothing will be downloaded). And suddenly you can find section ID in it's URL, for example http://testrails.url/index.php?/suites/view/124&group_by=cases:section_id&group_order=asc&group_id=3926 <-.

`exclude_suite_ids`
:   You can exclude any suites (even stated in *suite_ids*) from the document.

`exclude_section_ids`
:   The same with the sections. 

`exclude_case_ids`
:   And the same with the cases.

`filename`
:   Path to the test cases file. It should be added to project chapters in *foliant.yml*. Default: *test_cases.md*. For example:

```yaml
title: &title Test procedure

chapters:
    - intro.md
    - conditions.md
    - awesome_test_cases.md <- This one for test cases
    - appendum.md

preprocessors:
  - testrail:
    testrail_url: http://testrails.url
    testrail_login: username
    testrail_pass: password
    project_id: 35
    filename: awesome_test_cases.md
```

`rewrite_src_files`
:   You can update (*true*) test cases file after each use of preprocessor. Be careful, previous data will be deleted.

`template_folder`
:   Preprocessor uses Jinja2 templates to compose the file with test cases. Here you can find documentation: http://jinja.pocoo.org/docs/2.10/ . You can store templates in folder inside the foliant project, but if it's not default *case_templates* you have to write it here.

If this parameter not set and there is no default *case_templates* folder in the project, it will be created automatically with two jinja files for TestRail templates by default — *Test Case (Text)* with *template_id=1* and *Test Case (Steps)* with *template_id=2*.

You can create TestRail templates by yourself in *Administration* panel, *Customizations* section, *Templates* part. Then you have to create jinja templates whith the names *{template_id}.j2* for them. For example, file *2.j2* for *Test Case (Steps)* TestRail template:

```

{% if case['custom_steps_separated'][0]['content'] %}
{% if case['custom_preconds'] %}
**Preconditions:**

{{ case['custom_preconds'] }}
{% endif %}

**Scenario:**

{% for case_step in case['custom_steps_separated'] %}

*Step {{ loop.index }}.* {{ case_step['content'] }}

*Expected result:*

{{ case_step['expected'] }}

{% endfor %}
{% endif %}

```

You can use all parameters of two variables in the template — *case* and *params*. Case parameters depends on TestRail template. All custom parameters have prefix 'custom_' before system name set in TestRail.

Here is an example of *case* variable (parameters depends on case template):

```
case = {
    'created_by': 3,
    'created_on': 1524909903,
    'custom_expected': None,
    'custom_goals': None,
    'custom_mission': None,
    'custom_preconds': '- The user is not registered in the system.\r\n'
        '- Registration form opened.',
    'custom_steps': '',
    'custom_steps_separated': [{
        'content': 'Enter mobile phone number.',
        'expected': '- Entered phone number '
        'is visible in the form field.'
        },
        {'content': 'Press OK button.',
        'expected': '- SMS with registration code '
        'received.\n'}],
    'custom_test_androidtv': None,
    'custom_test_appletv': None,
    'custom_test_smarttv': 'None,
    'custom_tp': True,
    'estimate': None,
    'estimate_forecast': None,
    'id': 15940,
    'milestone_id': None,
    'priority_id': 4,
    'refs': None,
    'section_id': 3441,
    'suite_id': 101,
    'template_id': 7,
    'title': 'Registration by mobile phone number.',
    'type_id': 7,
    'updated_by': 10,
    'updated_on': 1528978979
}
```

And here is an example of *params* variable (parameters are always the same):

```
params = {
    'multi_param_name': 'platform',
    'multi_param_sys_name': 'custom_platform',
    'multi_param_select': ['android', 'ios'],
    'multi_param_select_type': any,
    'add_cases_without_multi_param': False,
    'checkbox_param_name': 'publish',
    'checkbox_param_sys_name': 'custom_publish',
    'checkbox_param_select_type': 'checked',
    'choose_priorities': ['critical', 'high', 'medium'],
    'add_multi_param_to_case_header': True,
    'add_multi_param_to_std_table': True,
    'add_priority_to_case_header': True,
    'add_priority_to_std_table': True,
    'add_case_id_to_case_header': False,
    'add_case_id_to_std_table': False,
    'links_to_images': [
        {'id': '123', 'link': '![Image caption](testrail_imgs/123.png)'},
        ...
    ]
}
```

`img_folder`
:   Folder to store downloaded images if `rewrite_src_files=True`.

`move_imgs_from_text`
:   It's impossible to compile test cases with images to the table. So you can use this parameter to convert image links in test cases to ordinary markdown-links and get the list with all image links in params['links_to_images'] parameter to use in jinja template. In this case you'll have to use [multilinetables](https://foliant-docs.github.io/docs/preprocessors/multilinetables/) and [anchors](https://foliant-docs.github.io/docs/preprocessors/anchors/) preprocessors.

For example, you have 2-step test case:

```
Step 1:

Press the button:

![Button](index.php?/attachments/get/741)

Result 1:

Dialog box will opened:

![Dialog box](index.php?/attachments/get/741)

Step 2:

Select option:

![List of options](index.php?/attachments/get/742)

Result 2:

Option selected:

![Result](index.php?/attachments/get/743)
```

Minimal *multilinetables* and *anchors* preprocessor settings in `foliant.yml` should be like this (more about *multilinetables* parameters see in [preprocessor documentation](https://foliant-docs.github.io/docs/preprocessors/multilinetables/)):

```
    - anchors
    - multilinetables:
        enable_hyphenation: true
        hyph_combination: brkln
        convert_to_grid: true
```

After *testrail* preprocessor process this test case, you will have `params['links_to_images']` parameter with list of image links in order of appearance to use in jinja template:

```yaml
[
    {'id': '740', 'link': '![Button](testrail_imgs/740.png)'},
    {'id': '741', 'link': '![Dialog box](testrail_imgs/741.png)'},
    {'id': '742', 'link': '![List of options](testrail_imgs/742.png)'},
    {'id': '743', 'link': '![Result](testrail_imgs/743.png)'}
]
```

Using this jinja template:

```
**Testing procedure:**

| # | Test step         | Expected result     | Passed   | Comment                |
|---|-------------------|---------------------|----------|------------------------|
{% for case_step in case['custom_steps_separated'] -%}
| {{ loop.index }} | {{ case_step['content']|replace("\n", "brkln") }} | {{ case_step['expected']|replace("\n", "brkln") }} |  |  |
{% endfor %}

{% if params['links_to_images'] %}
*Images:*

{% for image in params['links_to_images'] %}
<anchor>{{ image['id'] }}</anchor>

{{ image['link'] }}

{% endfor %}
{% endif %}
```

The markdown result will be:

```
**Testing procedure:**

+---+-----------------------------------------+----------------------------------------+--------+---------+
| # | Test step                               | Expected result                        | Passed | Comment |
+===+=========================================+========================================+========+=========+
| 1 | Press the button                        | Dialog box will opened:                |        |         |
|   |                                         |                                        |        |         |
|   | [Button](#740)                          | [Dialog box](#741)                     |        |         |
|   |                                         |                                        |        |         |
+---+-----------------------------------------+----------------------------------------+--------+---------+
| 2 | Select option:                          | Option selected:                       |        |         |
|   |                                         |                                        |        |         |
|   | [List of options](#742)                 | [Result](#743)                         |        |         |
+---+-----------------------------------------+----------------------------------------+--------+---------+

*Images:*

<anchor>740</anchor>

![Button](testrail_imgs/740.png)

<anchor>741</anchor>

![Dialog box](testrail_imgs/741.png)

<anchor>742</anchor>

![List of options](testrail_imgs/742.png)

<anchor>743</anchor>

![Result](testrail_imgs/743.png)
```

So you can use links in the table to go to the correspondent image.

> **Important!** Anchors must differ, so if one image (with the same image id) will appear in several test cases, this image will be downloaded separately for each appearance and renamed with postfix '-1', '-2', etc.

Next three fields are necessary due localization issues. While markdown document with test cases is composed on the go, you have to set up some document headers. Definitely not the best solution in my life. 

`section_header`
:   First level header of section with test cases. By default it's *Testing program* in Russian.

`std_table_header`
:   First level header of section with test results table. By default it's *Testing table* in Russian.

`std_table_column_headers`
:   Semicolon separated headers of testing table columns. By default it's *№; Priority; Platform; ID; Test case name; Result; Comment* in Russian.

`add_std_table`
:   You can exclude (*false*) a testing table from the document.

`add_suite_headers`
:   With *false* you can exclude all suite headers from the final document.

`add_section_headers`
:   With *false* you can exclude all section headers from the final document.

`add_case_id_to_case_header`
:   Every test case in TestRail has unique ID, which, as usual, you can find in the header or test case URL: http://testrails.url/index.php?/cases/view/15920... <-. So you can add (*true*) this ID to the test case headers and testing table. Or not (*false*).

`add_case_id_to_std_table`
:   Also you can add (*true*) the column with the test case IDs to the testing table.

In TestRail you can add custom parameters to your test case template. With next settings you can use one *multi-select* or *dropdown* (good for platforms, for example) and one *checkbox* (publishing) plus default *priority* parameter for cases sampling.

`multi_param_name`
:   Parameter name of *multi-select* or *dropdown* type you set in *System Name* field of *Add Custom Field* form in TestRail. For example, *platforms* with values *Android*, *iOS*, *PC*, *Mac* and *web*. If *multi_param_select* not set, all test cases will be downloaded (useful when you need just to add parameter value to the test headers or testing table).

`multi_param_select`
:   Here you can set the platforms for which you want to get test cases (case insensitive). For example, you have similar UX for mobile platforms and want to combine them:

```yaml
preprocessors:
  - testrail:
    ...
    multi_param_name: platforms
    multi_param_select: android, ios
    ...
```

`multi_param_select_type`
:   With this parameter you can make test cases sampling in different ways. It has several options:

- *any* (by default) — at least one of *multi_param_select* values should be set for the case,
- *all* — all of *multi_param_select* values should be set and any other can be set for the case,
- *only* — only *multi_param_select* values in any combination should be set for the case,
- *match* — all and only *multi_param_select* values should be set for the case.

With *multi_param_select: android, ios* we will get the following cases:

| Test cases  | Android | iOS | PC | Mac | web |   | any | all | only | match |
|-------------|:-------:|:---:|:--:|:---:|:---:|---|:---:|:---:|:----:|:-----:|
| Test case 1 |    +    |  +  |    |     |     |   |  +  |  +  |  +   |   +   |
| Test case 2 |    +    |  +  |    |     |     |   |  +  |  +  |  +   |   +   |
| Test case 3 |         |     | +  | +   |     |   |     |     |      |       |
| Test case 4 |         |  +  | +  | +   |     |   |  +  |     |      |       |
| Test case 5 |    +    |  +  |    |     |  +  |   |  +  |  +  |      |       |
| Test case 6 |    +    |  +  |    |     |  +  |   |  +  |  +  |      |       |
| Test case 7 |         |     | +  | +   |  +  |   |     |     |      |       |
| Test case 8 |         |     | +  | +   |  +  |   |     |     |      |       |
| Test case 9 |         |  +  |    |     |     |   |  +  |     |  +   |       |

`add_cases_without_multi_param`
:   Also you can include (by default) or exclude (*false*) cases without any value of *multi-select* or *dropdown* parameter.

`add_multi_param_to_case_header`
:   You can add (*true*) values of *multi-select* or *dropdown* parameter to the case headers or not (by default).

`add_multi_param_to_std_table`
:   You can add (*true*) column with values of *multi-select* or *dropdown* parameter to the testing table or not (by default).

`checkbox_param_name`
:   Parameter name of *checkbox* type you set in *System Name* field of *Add Custom Field* form in TestRail. For example, *publish*. Without parameter name set all of cases will be downloaded.

`checkbox_param_select_type`
:   With this parameter you can make test cases sampling in different ways. It has several options:

- *checked* (by default) — only cases whith checked field will be downloaded,
- *unchecked* — only cases whith unchecked field will be downloaded.

`choose_priorities`
:   Here you can set test case priorities to download (case insensitive).

```yaml
preprocessors:
  - testrail:
    ...
    choose_priorities: critical, high, medium
    ...
```

`add_priority_to_case_header`
:   You can add (*true*) priority to the case headers or not (by default).

`add_priority_to_std_table`
:   You can add (*true*) column with case priority to the testing table or not (by default).

Using described setting you can flexibly adjust test cases sampling. For example, you can download only published *critical* test cases for both and only *Mac* and *PC*.

Now strange things, mostly made specially for my project, but may be useful for others.

Screenshots. There is a possibility to store screenshots in TestRail test cases, but you can store them in the GitLab repository (link to which should be stated in one of the following parameters). GitLab project should have following structure:

```
images/
├── smarttv/
|   ├── screenshot1_smarttv.png
|   ├── screenshot2_smarttv.png
|   └── ...
├── androidtv/
|   ├── screenshot1_androidtv.png
|   ├── screenshot2_androidtv.png
|   └── ...
├── appletv/
|   ├── screenshot1_appletv.png
|   ├── screenshot2_appletv.png
|   └── ...
├── web/
|   ├── screenshot1_web.png
|   ├── screenshot2_web.png
|   └── ...
├── screenshot1.png
├── screenshot2.png
└── ...
```

*images* folder used for projects without platforms.

Filename ending is a first value of *multi_param_select* parameter (*platform*). Now to add screenshot to your document just add following string to the test case (unfortunately, in TestRail interface it will looks like broken image link):

```
(leading exclamation mark here!)[Image title](main_filename_part)
```

Preprocessor will convert to the following format:

```
https://gitlab.url/gitlab_group_name/gitlab_project_name/raw/master/images/platform_name/main_filename_part_platform_name.png
```

For example, in the project with *multi_param_select: smarttv* the string

```
(leading exclamation mark here!)[Application main screen](main_screen)
```

will be converted to:

```
(leading exclamation mark here!)[Application main screen](https://gitlab.url/documentation/application-screenshots/raw/master/images/smarttv/main_screen_smarttv.png)
```

That's it.

`resolve_urls`
:   Turn on (*true*) or off (*false*, by default) image urls resolving.

`screenshots_url`
:   GitLab repository URL, in our example: https://gitlab.url/documentation/application-screenshots/ .

`img_ext`
:   Screenshots extension. Yes, it must be only one and the same for all screenshots. Also this parameter used to save downloaded images from TestRail.

And the last one emergency tool. If you have no jinja template for any type of TestRail case, you'll see this message like this: *There is no jinja template for test case template_id 5 (case_id 1325) in folder case_templates*. So you have to write jinja template by yourself. To do this it's necessary to know case structure. This parameter shows it to you.

`print_case_structure`
:   Turn on (*true*) or off (*false*, by default) printing out of case structure with all data in it if any problem occurs.


## Usage

Just add the preprocessor to the project config, set it up and enjoy the automatically collected test cases to your document.


### Tips

In some cases you may encounter a problem with test cases text format, so composed markdown file will be converted to the document with bad formatting. In this cases *replace* preprocessor could be useful: https://foliant-docs.github.io/docs/preprocessors/replace/ .
