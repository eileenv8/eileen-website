import { getBlogPosts, getFeaturedPhotos, getAboutMe } from '../lib/sanity'
import { urlFor } from '../lib/sanity'
import Image from 'next/image'
import Link from 'next/link'

export default async function Home() {
  // Fetch data from Sanity
  const aboutMe = await getAboutMe()
  const blogPosts = await getBlogPosts()
  const featuredPhotos = await getFeaturedPhotos()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Eileen&apos;s Website</h1>
          <nav className="mt-4">
            <div className="flex space-x-8">
              <Link href="/" className="text-gray-900 hover:text-gray-600">Home</Link>
              <Link href="/blog" className="text-gray-600 hover:text-gray-900">Blog</Link>
              <Link href="/photos" className="text-gray-600 hover:text-gray-900">Photos</Link>
              <Link href="/library" className="text-gray-600 hover:text-gray-900">Library</Link>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* About Me Section */}
        {aboutMe && (
          <section className="mb-16">
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
              <div className="md:flex">
                {aboutMe.profileImage && (
                  <div className="md:w-1/3">
                    <div className="aspect-square relative">
                      <Image
                        src={urlFor(aboutMe.profileImage).width(400).height(400).url()}
                        alt={aboutMe.title}
                        fill
                        className="object-cover"
                      />
                    </div>
                  </div>
                )}
                <div className={`p-8 ${aboutMe.profileImage ? 'md:w-2/3' : 'w-full'}`}>
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">{aboutMe.title}</h2>
                  
                  {aboutMe.highlights && aboutMe.highlights.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-4">
                      {aboutMe.highlights.map((highlight, index) => (
                        <span 
                          key={index}
                          className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                        >
                          {highlight}
                        </span>
                      ))}
                    </div>
                  )}
                  
                  <p className="text-gray-700 text-lg leading-relaxed mb-6">
                    {aboutMe.bio}
                  </p>
                  
                  <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-600 mb-6">
                    {aboutMe.location && (
                      <div className="flex items-center">
                        <span className="mr-2">📍</span>
                        <span>{aboutMe.location}</span>
                      </div>
                    )}
                    {aboutMe.currentProject && (
                      <div className="flex items-center">
                        <span className="mr-2">🚀</span>
                        <span>Currently: {aboutMe.currentProject}</span>
                      </div>
                    )}
                    {aboutMe.contactEmail && (
                      <div className="flex items-center">
                        <span className="mr-2">✉️</span>
                        <a 
                          href={`mailto:${aboutMe.contactEmail}`}
                          className="text-blue-600 hover:text-blue-800"
                        >
                          {aboutMe.contactEmail}
                        </a>
                      </div>
                    )}
                  </div>
                  
                  {aboutMe.socialLinks && (
                    <div className="flex space-x-4">
                      {aboutMe.socialLinks.twitter && (
                        <a 
                          href={aboutMe.socialLinks.twitter}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-500 hover:text-blue-700"
                        >
                          Twitter
                        </a>
                      )}
                      {aboutMe.socialLinks.instagram && (
                        <a 
                          href={aboutMe.socialLinks.instagram}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-pink-500 hover:text-pink-700"
                        >
                          Instagram
                        </a>
                      )}
                      {aboutMe.socialLinks.github && (
                        <a 
                          href={aboutMe.socialLinks.github}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-gray-700 hover:text-gray-900"
                        >
                          GitHub
                        </a>
                      )}
                      {aboutMe.socialLinks.linkedin && (
                        <a 
                          href={aboutMe.socialLinks.linkedin}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800"
                        >
                          LinkedIn
                        </a>
                      )}
                      {aboutMe.socialLinks.website && (
                        <a 
                          href={aboutMe.socialLinks.website}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-green-600 hover:text-green-800"
                        >
                          Website
                        </a>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </section>
        )}
       

        {/* Recent Blog Posts */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Blog Posts</h2>
          {blogPosts.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {blogPosts.slice(0, 3).map((post) => (
                <article key={post._id} className="bg-white rounded-lg shadow-md overflow-hidden">
                  {post.featuredImage && (
                    <div className="aspect-video relative">
                      <Image
                        src={urlFor(post.featuredImage).width(400).height(225).url()}
                        alt={post.title}
                        fill
                        className="object-cover"
                      />
                    </div>
                  )}
                  <div className="p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      <Link href={`/blog/${post.slug.current}`} className="hover:text-blue-600">
                        {post.title}
                      </Link>
                    </h3>
                    {post.excerpt && (
                      <p className="text-gray-600 mb-3">{post.excerpt}</p>
                    )}
                    <div className="text-sm text-gray-500">
                      {new Date(post.publishedAt).toLocaleDateString()}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <p className="text-gray-600">No blog posts yet. Create some in your Sanity studio!</p>
          )}
        </section>

        {/* Featured Photos */}
        {featuredPhotos.length > 0 && (
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Featured Photos</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              {featuredPhotos.slice(0, 4).map((photo) => (
                <div key={photo._id} className="bg-white rounded-lg shadow-md overflow-hidden">
                  <div className="aspect-square relative">
                    <Image
                      src={urlFor(photo.image).width(300).height(300).url()}
                      alt={photo.title || 'Photo'}
                      fill
                      className="object-cover"
                    />
                  </div>
                  {(photo.title || photo.location) && (
                    <div className="p-3">
                      {photo.title && (
                        <h3 className="font-medium text-gray-900">{photo.title}</h3>
                      )}
                      {photo.location && (
                        <p className="text-sm text-gray-600">{photo.location}</p>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

      </main>
    </div>
  )
}