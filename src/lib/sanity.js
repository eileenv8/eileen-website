import {createClient} from '@sanity/client'
import imageUrlBuilder from '@sanity/image-url'

export const client = createClient({
  projectId: 'uvdkkjro',
  dataset: 'production',
  useCdn: true,
  apiVersion: '2023-01-01'
})

// Helper for generating image URLs
const builder = imageUrlBuilder(client)
export const urlFor = (source) => builder.image(source)

// Blog post queries
export const getBlogPosts = () => {
  return client.fetch(`
    *[_type == "blogPost" && draft != true] | order(publishedAt desc) {
      title,
      slug,
      author,
      publishedAt,
      excerpt,
      featuredImage,
      tags,
      _id
    }
  `)
}

export const getBlogPost = (slug) => {
  return client.fetch(`
    *[_type == "blogPost" && slug.current == $slug][0] {
      title,
      slug,
      author,
      publishedAt,
      excerpt,
      featuredImage,
      content,
      tags,
      _id
    }
  `, { slug })
}

// Photo queries
export const getPhotos = () => {
  return client.fetch(`
    *[_type == "photo"] | order(takenAt desc) {
      title,
      image,
      caption,
      location,
      takenAt,
      tags,
      camera,
      featured,
      _id
    }
  `)
}

export const getFeaturedPhotos = () => {
  return client.fetch(`
    *[_type == "photo" && featured == true] | order(takenAt desc) {
      title,
      image,
      caption,
      location,
      takenAt,
      tags,
      camera,
      _id
    }
  `)
}

// File library queries
export const getFileLibrary = () => {
  return client.fetch(`
    *[_type == "fileLibrary"] | order(dateAdded desc) {
      title,
      slug,
      file,
      description,
      author,
      source,
      sourceUrl,
      dateAdded,
      publicationDate,
      tags,
      category,
      featured,
      rating,
      _id
    }
  `)
}

export const getFeaturedFiles = () => {
  return client.fetch(`
    *[_type == "fileLibrary" && featured == true] | order(dateAdded desc) {                                      esc) {
      title,
      slug,
      file,
      description,
      author,
      category,
      rating,
      _id
    }
  `)
} 

export const getAboutMe = () => {
  return client.fetch(`
    *[_type == "aboutMe"][0] {
      title,
      profileImage,
      bio,
      highlights,
      location,
      currentProject,
      contactEmail,
      socialLinks
    }
  `)
}