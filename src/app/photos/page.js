import { getPhotos } from '../../lib/sanity'
import { urlFor } from '../../lib/sanity'
import Image from 'next/image'
import Link from 'next/link'

export default async function PhotosPage() {
  const photos = await getPhotos()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Eileen&apos;s Website</h1>
          <nav className="mt-4">
            <div className="flex space-x-8">
              <Link href="/" className="text-gray-600 hover:text-gray-900">Home</Link>
              <Link href="/blog" className="text-gray-600 hover:text-gray-900">Blog</Link>
              <Link href="/photos" className="text-gray-900 hover:text-gray-600">Photos</Link>
              <Link href="/library" className="text-gray-600 hover:text-gray-900">Library</Link>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Photo Stream</h1>
        
        {photos.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {photos.map((photo) => (
              <div key={photo._id} className="bg-white rounded-lg shadow-md overflow-hidden group">
                <div className="aspect-square relative">
                  <Image
                    src={urlFor(photo.image).width(400).height(400).url()}
                    alt={photo.title || 'Photo'}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  {photo.featured && (
                    <div className="absolute top-2 right-2 bg-yellow-400 text-yellow-900 px-2 py-1 rounded-full text-xs font-semibold">
                      ⭐ Featured
                    </div>
                  )}
                </div>
                
                {(photo.title || photo.caption || photo.location) && (
                  <div className="p-4">
                    {photo.title && (
                      <h3 className="font-semibold text-gray-900 mb-1">{photo.title}</h3>
                    )}
                    {photo.caption && (
                      <p className="text-gray-600 text-sm mb-2">{photo.caption}</p>
                    )}
                    
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      {photo.location && (
                        <span className="flex items-center">
                          📍 {photo.location}
                        </span>
                      )}
                      {photo.takenAt && (
                        <span>{new Date(photo.takenAt).toLocaleDateString()}</span>
                      )}
                    </div>
                    
                    {photo.tags && photo.tags.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-2">
                        {photo.tags.slice(0, 3).map((tag, index) => (
                          <span 
                            key={index}
                            className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <h2 className="text-2xl font-semibold text-gray-600 mb-4">No photos yet</h2>
            <p className="text-gray-500">Upload some photos in your Sanity studio!</p>
          </div>
        )}
      </main>
    </div>
  )
}