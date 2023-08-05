from demisto_sdk.commands.common.git_tools import git_path

GIT_ROOT = "{}".format(git_path())
INVALID_PLAYBOOK_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/Playbooks.playbook-invalid.yml"
VALID_TEST_PLAYBOOK_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/Playbooks.playbook-test.yml"
VALID_BETA_PLAYBOOK_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/beta-playbook-valid.yml"
VALID_PLAYBOOK_ARCSIGHT_ADD_DOMAIN_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/Playbooks." \
                                          f"playbook-ArcSight_Add_Domain_Indicators.yml"
INVALID_INTEGRATION_NO_TESTS = f'{GIT_ROOT}/demisto_sdk/tests/test_files/non-valid-integration-no-test-playbooks.yml'
INVALID_INTEGRATION_NON_CONFIGURED_TESTS = f'{GIT_ROOT}/demisto_sdk/tests/test_files/' \
                                           f'non-valid-integration-test-not-configured.yml'
TEST_PLAYBOOK = f'{GIT_ROOT}/demisto_sdk/tests/test_files/playbook-TestPlaybooks.yml'
VALID_INTEGRATION_TEST_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-test.yml"
INVALID_INTEGRATION_WITH_NO_TEST_PLAYBOOK = 'demisto_sdk/tests/test_files/integration-test-with-no-test-playbook.yml'
VALID_INTEGRATION_ID_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-valid-id-test.yml"
INVALID_INTEGRATION_ID_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-id-test.yml"
INVALID_PLAYBOOK_PATH_FROM_ROOT = f"{GIT_ROOT}/demisto_sdk/tests/test_files/playbook-disconnected_from_root.yml"
VALID_PLAYBOOK_ID_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/playbook-valid-id-test.yml"
INVALID_PLAYBOOK_ID_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/playbook-invalid-id-test.yml"
INVALID_PLAYBOOK_CONDITION_1 = f"{GIT_ROOT}/demisto_sdk/tests/test_files/playbook-Invalid_condition_unhandled_" \
                               f"branch.yml"
INVALID_IGNORED_UNIFIED_INTEGRATION = f'{GIT_ROOT}/demisto_sdk/tests/test_files/integration_ignored_invalid_unified.yml'
SCRIPT_WITH_PLAYBOOK = 'demisto_sdk/tests/test_files/script-with-test-playbook.yml'
INVALID_PLAYBOOK_CONDITION_2 = f"{GIT_ROOT}/demisto_sdk/tests/test_files/playbook-Invalid_condition_unhandled_" \
                               f"branch_and_unhandled_condition.yml"
VALID_PLAYBOOK_CONDITION = f"{GIT_ROOT}/demisto_sdk/tests/test_files/playbook-valid_condition.yml"
VALID_REPUTATION_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/reputations-valid.json"
INVALID_REPUTATION_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/reputations-invalid.json"
VALID_LAYOUT_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/layout-valid.json"
INVALID_LAYOUT_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/layout-invalid.json"
VALID_INCIDENT_TYPE_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/incidenttype-valid.json"
VALID_WIDGET_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/widget-valid.json"
INVALID_WIDGET_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/widget-invalid.json"
VALID_DASHBOARD_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/dashboard-valid.json"
INVALID_DASHBOARD_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/dashboard-invalid.json"
VALID_INCIDENT_FIELD_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/incidentfield-valid.json"
INVALID_INCIDENT_FIELD_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/incidentfield-invalid.json"
VALID_INDICATOR_FIELD_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/indicatorfield-valid.json"
INVALID_WIDGET_VERSION_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/widget-invalid-version.json"
VALID_SCRIPT_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/script-valid.yml"
INVALID_SCRIPT_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/script-invalid.yml"
VALID_ONE_LINE_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/valid-one-line_CHANGELOG.md"
VALID_ONE_LINE_LIST_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/valid-one-line-list_CHANGELOG.md"
VALID_MULTI_LINE_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/valid-multi-line_CHANGELOG.md"
VALID_MULTI_LINE_LIST_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/valid-multi-line-list_CHANGELOG.md"
INVALID_ONE_LINE_1_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-one-line_1_CHANGELOG.md"
INVALID_ONE_LINE_2_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-one-line_2_CHANGELOG.md"
INVALID_ONE_LINE_LIST_1_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-one-line-list_1_CHANGELOG.md"
INVALID_ONE_LINE_LIST_2_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-one-line-list_2_CHANGELOG.md"
INVALID_MULTI_LINE_1_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-multi-line_1_CHANGELOG.md"
INVALID_MULTI_LINE_2_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-multi-line_2_CHANGELOG.md"
LAYOUT_TARGET = "./Layouts/layout-mock.json"
INDICATOR_TYPE_TARGET = "IndicatorTypes/reputations-valid.json"
WIDGET_TARGET = "./Widgets/widget-mocks.json"
DASHBOARD_TARGET = "./Dashboards/dashboard-mocks.json"
PLAYBOOK_TARGET = "Playbooks/playbook-test.yml"
INTEGRATION_TARGET = "./Integrations/integration-test.yml"
INCIDENT_FIELD_TARGET = "IncidentFields/incidentfield-test.json"
INCIDENT_TYPE_TARGET = "IncidentTypes/incidenttype-valid.json"
PLAYBOOK_PACK_TARGET = "Packs/Int/Playbooks/playbook-test.yml"
INVALID_TEST_PLAYBOOK_UNHANDLED_CONDITION = f'{GIT_ROOT}/demisto_sdk/tests/test_files/content_repo_example/Packs/' \
                                            f'FeedAzure/TestPlaybooks/playbook-FeedAzure_test_copy_no_prefix.yml'
INVALID_PLAYBOOK_UNHANDLED_CONDITION = f'{GIT_ROOT}/demisto_sdk/tests/test_files/content_repo_example/Packs/' \
                                       f'FeedAzure/Playbooks/FeedAzure_test.yml'
SCRIPT_TARGET = "./Scripts/script-test.yml"
BETA_INTEGRATION_TARGET = "./Beta_Integrations/integration-test.yml"
SCRIPT_RELEASE_NOTES_TARGET = "./Scripts/script-test_CHANGELOG.md"
INTEGRATION_RELEASE_NOTES_TARGET = "./Integrations/integration-test_CHANGELOG.md"
SOURCE_FORMAT_INTEGRATION_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_New_Integration_copy.yml"
DESTINATION_FORMAT_INTEGRATION_COPY = "new_format_New_Integration_copy.yml"
SOURCE_FORMAT_SCRIPT_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_New_script_copy.yml"
DESTINATION_FORMAT_SCRIPT_COPY = "new_format_New_script_copy.yml"
SOURCE_FORMAT_PLAYBOOK_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_new_playbook_copy.yml"
DESTINATION_FORMAT_PLAYBOOK_COPY = "playbook-new_format_new_playbook_copy.yml"
INTEGRATION_WITH_TEST_PLAYBOOKS = f'{GIT_ROOT}/demisto_sdk/tests/test_files/format_Integration_with_test_playbooks.yml'
PLAYBOOK_WITH_TEST_PLAYBOOKS = f'{GIT_ROOT}/demisto_sdk/tests/test_files/format_playbook_with_test_playbooks.yml'
SCRIPT_WITH_TEST_PLAYBOOKS = f'{GIT_ROOT}/demisto_sdk/tests/test_files/format_script_with_test_playbooks.yml'
INDICATORFIELD_EXTRA_FIELDS = f"{GIT_ROOT}/demisto_sdk/tests/test_files/indicatorfield-extra-fields.json"
INDICATORFIELD_EXACT_SCHEME = f"{GIT_ROOT}/demisto_sdk/tests/test_files/indicator-field-exact-scheme.json"
INDICATORFIELD_MISSING_FIELD = f"{GIT_ROOT}/demisto_sdk/tests/test_files/indicator-field-missing-field.json"
INDICATORFIELD_MISSING_AND_EXTRA_FIELDS = f"{GIT_ROOT}/demisto_sdk/tests/test_files/" \
                                          f"indicatorfield-missing-and-extra-fields.json"
INVALID_INTEGRATION_YML_1 = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-yml1.yml"
INVALID_INTEGRATION_YML_2 = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-yml2.yml"
INVALID_INTEGRATION_YML_3 = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-yml3.yml"
INVALID_INTEGRATION_YML_4 = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-yml4.yml"
VALID_REPUTATION_FILE = f"{GIT_ROOT}/demisto_sdk/tests/test_files/reputation-cidr-valid.json"
INVALID_REPUTATION_FILE = f"{GIT_ROOT}/demisto_sdk/tests/test_files/reputation-cidr-invalid.json"
EQUAL_VAL_FORMAT_PLAYBOOK_SOURCE = f"{GIT_ROOT}/demisto_sdk/tests/test_files/playbook-invalid-equal.yml"
EQUAL_VAL_FORMAT_PLAYBOOK_DESTINATION = "Playbooks/playbook-invalid-equal.yml"
EQUAL_VAL_PATH = 'Playbooks'
INVALID_NO_HIDDEN_PARAMS = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-no-hidden-params.yml"
VALID_NO_HIDDEN_PARAMS = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-valid-no-unallowed-hidden-params.yml"
GIT_HAVE_MODIFIED_AND_NEW_FILES = f"{GIT_ROOT}/demisto_sdk/tests/test_files/git_have_modified_and_new_files.json"
SOURCE_FORMAT_INCIDENTFIELD_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_incidentfield-copy.json"
DESTINATION_FORMAT_INCIDENTFIELD_COPY = "IncidentFields/incidentfield-copy.json"
INCIDENTFIELD_PATH = "IncidentFields"
SOURCE_FORMAT_INCIDENTTYPE_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_incidenttype-copy.json"
DESTINATION_FORMAT_INCIDENTTYPE_COPY = "IncidentTypes/incidenttype-copy.json"
INCIDENTTYPE_PATH = "IncidentTypes"

SOURCE_FORMAT_INDICATORFIELD_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_indicatorfield-copy.json"
DESTINATION_FORMAT_INDICATORFIELD_COPY = "IndicatorFields/incidentfield-copy.json"
INDICATORFIELD_PATH = "IndicatorFields"

SOURCE_FORMAT_INDICATORTYPE_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_indicatortype-copy.json"
DESTINATION_FORMAT_INDICATORTYPE_COPY = "Packs/Base/Misc/reputation-copy.json"
INDICATORTYPE_PATH = "Packs/Base/Misc"

SOURCE_FORMAT_LAYOUT_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_layout-copy.json"
DESTINATION_FORMAT_LAYOUT_COPY = "Layouts/layout-copy.json"
LAYOUT_PATH = "Layouts"

SOURCE_FORMAT_DASHBOARD_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_dashboard-copy.json"
DESTINATION_FORMAT_DASHBOARD_COPY = "Dashboards/dashboard-copy.json"
DASHBOARD_PATH = "Dashboards"

SOURCE_FORMAT_PLAYBOOK = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_playbook.yml"
DESTINATION_FORMAT_PLAYBOOK = "Playbook/playbook.yml"
PLAYBOOK_PATH = "Playbook"

VALID_MD = f'{git_path()}/demisto_sdk/tests/test_files/README-valid.md'
INVALID_MD = f'{git_path()}/demisto_sdk/tests/test_files/README-invalid.md'

DEFAULT_IMAGE = f'{git_path()}/demisto_sdk/tests/test_files/default_image.png'
VALID_PACK = f'{git_path()}/demisto_sdk/tests/test_files/content_repo_example/Packs/FeedAzure'
VALID_PACK_RELATIVE_PATH = 'Packs/FeedAzure'
VALID_BETA_INTEGRATION = f'{git_path()}/demisto_sdk/tests/test_files/valid-beta-integration.yml'

INVALID_OUTPUT_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files"
CONF_JSON_MOCK_PATH = 'demisto_sdk/tests/test_files/conf.json'
