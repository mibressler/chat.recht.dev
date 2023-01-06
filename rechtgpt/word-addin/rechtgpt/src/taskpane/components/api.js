import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

// Define a service using a base URL and expected endpoints
export const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: 'https://api.recht.dev/' }),
  endpoints: (builder) => ({
    getReferences: builder.query({
      query: (prompt) => `reference?prompt=${prompt}`,
    }),
    getRuling: builder.query({
        query: (id) => `ruling?id=${id}`,
    })
  }),
})

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const { useLazyGetReferencesQuery, useLazyGetRulingQuery } = api
