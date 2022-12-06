package rig.sqlms.controller;


import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.skyscreamer.jsonassert.JSONAssert;
import rig.sqlms.BaseIntegrationTest;

import java.time.OffsetDateTime;
import java.util.Locale;
import java.util.stream.IntStream;

import static java.lang.String.format;
import static java.util.stream.Collectors.joining;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.skyscreamer.jsonassert.JSONCompareMode.LENIENT;
import static org.skyscreamer.jsonassert.JSONCompareMode.STRICT;
import static org.springframework.http.MediaType.APPLICATION_JSON;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class QueryControllerIntegrationTest extends BaseIntegrationTest {

    @Test
    void execute_shouldHandleSelectWithMultipleResults() throws Exception {
        String responseBody = mockMvc.perform(post("/get-users"))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        JSONAssert.assertEquals("""
                [
                  {
                    "id": -2,
                    "email": "user@example.com",
                    "name": "User Name",
                    "passwordHash": "$2a$12$AXElLQmIKy1EZVSrlO2HnO0dTsHcf4LstadG7a5arYXUAGf5VCeZm",
                    "login": "user"
                  },
                  {
                    "id": -1,
                    "email": "admin@example.com",
                    "name": "Admin Name",
                    "passwordHash": "$2a$12$YlbrvfwwznrmQNM71UFFvO3krrFnUsKvGcN5zNDBNMpD2w9WDqHuO",
                    "login": "admin"
                  }
                ]""", responseBody, STRICT);
    }

    @Test
    void execute_shouldHandleSelectWithParameters() throws Exception {
        String responseBody = mockMvc.perform(post("/get-user-email-by-login")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"login": "%s"}""".formatted(ADMIN_LOGIN)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        JSONAssert.assertEquals("""
                [{"email": "%s"}]""".formatted(ADMIN_EMAIL), responseBody, STRICT);
    }

    @Test
    @Disabled("Timestamp problem with h2, but not with postgres. Enable when testcontainers used for testing.")
    void execute_shouldHandleInsertWithParameters() throws Exception {
        String dueBy = "2021-11-26T14:52:32.748Z";
        double amount = 121.79;

        String responseBody = mockMvc.perform(post("/add-debt")
                        .contentType(APPLICATION_JSON)
                        .content(format(Locale.ENGLISH, """
                                {
                                  "userId": %d,
                                  "amount": %f,
                                  "dueBy": "%s"
                                }""", ADMIN_ID, amount, dueBy)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        JSONAssert.assertEquals("[]", responseBody, STRICT);

        responseBody = mockMvc.perform(post("/get-debt-by-user-id")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"userId": %d}""".formatted(ADMIN_ID)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        JSONAssert.assertEquals("""
                [
                  {
                    "userId": -1,
                    "amount": 121.79,
                    "dueBy": "2021-11-26T14:52:32.748+00:00"
                  }
                ]""", responseBody, LENIENT);
    }

    @Test
    void execute_shouldHandleUpdateWithParameters() throws Exception {
        String updatedEmail = "updated@email.com";
        mockMvc.perform(post("/update-user-email-by-login")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {
                                  "login": "%s",
                                  "email": "%s"
                                }""".formatted(ADMIN_LOGIN, updatedEmail)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("length()").value(0));

        mockMvc.perform(post("/get-user-email-by-login")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"login": "%s"}""".formatted(ADMIN_LOGIN)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("length()").value(1))
                .andExpect(jsonPath("$.[0].email").value(updatedEmail));
    }

    @Test
    void execute_shouldHandleDatabaseFunctionsInSavedQuery() throws Exception {
        String responseBody = mockMvc.perform(post("/get-uppercase-user-email-by-login")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"login": "%s"}""".formatted(ADMIN_LOGIN)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        JSONAssert.assertEquals("""
                [{"email": "%s"}]""".formatted(ADMIN_EMAIL.toUpperCase()), responseBody, STRICT);
    }

    @Test
    void execute_shouldHandleNullValueParameter() throws Exception {
        String responseBody = mockMvc.perform(post("/get-user-email-by-login")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"login": null}"""))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        JSONAssert.assertEquals("[]", responseBody, STRICT);
    }

    @Test
    @Disabled("Timestamp problem with h2, but not with postgres. Enable when testcontainers used for testing.")
    void execute_shouldHandleArrayInResult() throws Exception {
        mockMvc.perform(post("/add-debt")
                        .contentType(APPLICATION_JSON)
                        .content(format(Locale.ENGLISH, """
                                {
                                  "userId": %d,
                                  "amount": 10,
                                  "dueBy": "2021-11-26T14:52:32.748Z"
                                }""", ADMIN_ID)))
                .andExpect(status().isOk());
        mockMvc.perform(post("/add-debt")
                        .contentType(APPLICATION_JSON)
                        .content(format(Locale.ENGLISH, """
                                {
                                  "userId": %d,
                                  "amount": 10,
                                  "dueBy": "2022-12-22T12:22:22.222Z"
                                }""", ADMIN_ID)))
                .andExpect(status().isOk());

        String responseBody = mockMvc.perform(post("/get-debt-due-dates-by-user-id")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"userId": %d}""".formatted(ADMIN_ID)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        String expectedResponse = format("""
                [{"userId": %d, "dueDates": ["2021-11-26T14:52:32.748+00:00", "2022-12-22T12:22:22.222+00:00"]}]""", ADMIN_ID);
        JSONAssert.assertEquals(expectedResponse, responseBody, STRICT);
    }

    @Test
    void execute_shouldNotHaveAResultLimit() throws Exception {
        String queries = IntStream.range(0, 101)
                .mapToObj(i -> """
                        {
                          "userId": %d,
                          "amount": %d,
                          "dueBy": "%s"
                        }""".formatted(ADMIN_ID, i, OffsetDateTime.now()))
                .collect(joining(","));

        mockMvc.perform(post("/add-debt/batch")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"queries": [%s]}""".formatted(queries)))
                .andExpect(status().isOk());

        mockMvc.perform(post("/get-debt-by-user-id")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"userId": %d}""".formatted(ADMIN_ID)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("length()").value(101));
    }

    @Test
    void execute_shouldReturnCompactJson() throws Exception {
        String responseBody = mockMvc.perform(post("/get-user-email-by-login")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"login": "%s"}""".formatted(ADMIN_LOGIN)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        assertEquals("""
                [{"email":"%s"}]""".formatted(ADMIN_EMAIL), responseBody);
    }

    @Test
    void execute_shouldNotAllowEscapingOutOfTemplateParameters() throws Exception {
        String responseBody = mockMvc.perform(post("/get-user-email-by-login")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"login": "admin'OR(1=1)--"}"""))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        JSONAssert.assertEquals("[]", responseBody, STRICT);
    }

    @Test
    void execute_shouldThrowWhenQueryNotFound() throws Exception {
        String responseBody = mockMvc.perform(post("/unknown"))
                .andExpect(status().is4xxClientError())
                .andReturn().getResponse().getContentAsString();

        JSONAssert.assertEquals("""
                {"error":"ResqlRuntimeException","message":"Saved query 'unknown' does not exist"}""", responseBody, STRICT);
    }

    @Test
    void execute_shouldThrowOnUnknownTable() throws Exception {
        mockMvc.perform(post("/get-unknown-table"))
                .andExpect(status().is4xxClientError())
                .andExpect(jsonPath("$.error").value("BadSqlGrammarException"));
    }

    @Test
    void execute_shouldThrowOnMissingParameter() throws Exception {
        mockMvc.perform(post("/get-user-email-by-login"))
                .andExpect(status().is4xxClientError())
                .andExpect(jsonPath("$.error").value("InvalidDataAccessApiUsageException"))
                .andExpect(jsonPath("$.message").value("No value supplied for the SQL parameter 'login': No value registered for key 'login'"));
    }


    @Test
    void execute_shouldThrowWhenDataSourceNotConfigured() throws Exception {
        mockMvc.perform(post("/no-datasource-configured"))
                .andExpect(status().is4xxClientError())
                .andExpect(jsonPath("$.error").value("UnknownDataSourceNameException"))
                .andExpect(jsonPath("$.message").value("Specified dataSourceName name: 'no-datasource-configured' is unknown to the service"));
    }

    @Test
    void executeBatch_shouldHandleMultipleSelectWithParameters() throws Exception {
        String responseBody = mockMvc.perform(post("/get-user-email-by-login/batch")
                        .contentType(APPLICATION_JSON)
                        .content("""
                                {"queries": [{"login": "%s"},{"login": "%s"}]}""".formatted(ADMIN_LOGIN, USER_LOGIN)))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();

        JSONAssert.assertEquals("""
                [[{"email": "%s"}], [{"email": "%s"}]]""".formatted(ADMIN_EMAIL, USER_EMAIL), responseBody, STRICT);
    }
}
