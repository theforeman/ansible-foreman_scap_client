#!/usr/bin/ruby
require 'rubygems' if RUBY_VERSION.start_with? '1.8'
require 'json'

def subscription_manager_cert_paths
  certificates = {}
  certificate_end_path = '/cert.pem'
  private_key_end_path = '/key.pem'
  data = nil
  begin
    data = `subscription-manager config`
  rescue Errno::ENOENT => e
    return certificates
  end
  return certificates unless $?.success? && data
  data = data.gsub("\n", "").gsub(/[\[\]]/, "")
  data_array = data.scan(/(\S+)\s*=\s* ([^ ]+)/)
  data_hash = Hash[*data_array.flatten]
  consumer_cert_dir = data_hash["consumercertdir"]
  certificates[:rh_ca_cert_path] = data_hash["repo_ca_cert"]
  certificates[:rh_consumer_cert_path] = consumer_cert_dir + certificate_end_path
  certificates[:rh_consumer_private_key_path] = consumer_cert_dir + private_key_end_path

  certificates
end

print subscription_manager_cert_paths.to_json
